import json
import os
from typing import Optional, Dict, Any, List, AsyncGenerator
from contextlib import AsyncExitStack

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import log
import time
import uuid
from prompt import tool_caller_system_prompt, replier_system_prompt
from fastapi.responses import StreamingResponse
from data.meta_data import chain_id_map
logging = log.Logger("client_service").get_logger()

MAX_MSG_LENGTH = 10
MAX_ROUNDS = 10
MAX_CALL_PER_ROUND = 5

load_dotenv()

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    address: Optional[str] = None
    chainid: Optional[str] = None
    msg: List[Message]

class MCPClient:
    def __init__(self, address: str = None, chainid: str=56):
        self.address = address
        self.chainid = chainid
        self.chain = chain_id_map.get(self.chainid, self.chainid)
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = OpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"))
        self.replier_client = OpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"))
        self.chat_id = str(uuid.uuid4())
        self.tool_call_count = 0
        self.on_chain_calls = []
        self.tools_called = []
        self.tool_caller_llm_use_time = 0
        self.reply_llm_use_time = 0
        self.onChain_tool_called = False
        self.available_tools = []
        self.messages = [{"role": "system", "content": tool_caller_system_prompt}]
        wallet_info= f"User's address is {self.address}. User's wallet is currently active on {self.chain} chain, chainid is {self.chainid}."
        self.messages.append({"role": "system", "content": wallet_info})

    async def connect_to_server(self):
        server_params = StdioServerParameters(
            command='uv',
            args=['run', 'mcp_proxy.py'],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params))
        stdio, write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(stdio, write))

        await self.session.initialize()

    async def process_messages(self, msg: List[Dict[str, str]]):
        if len(msg) > MAX_MSG_LENGTH:
            msg = msg[-MAX_MSG_LENGTH:]
            logging.info(f"Chat_id={self.chat_id} ｜msg length={len(msg)} decreased to {MAX_MSG_LENGTH}")

        self.messages.extend(msg)
    
    async def get_available_tools(self):
        response = await self.session.list_tools()
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
        } for tool in response.tools]
        return available_tools
    
    async def _call_replier(self):
        t_reply = time.time()
        logging.info(f"Chat_id={self.chat_id} - Calling replier model")
        self.messages[0] = {"role": "system", "content": replier_system_prompt}
        
        # 启用流式响应
        response = self.replier_client.chat.completions.create(
            model=os.getenv("LLM_MODEL"),
            messages=self.messages,
            stream=True  # 关键修改：启用流模式
        )
        
        content = []
        for chunk in response:
            if chunk.choices[0].delta.content:
                chunk_content = chunk.choices[0].delta.content
                content.append(chunk_content)
                # 包装为结构化数据
                yield f"data: {json.dumps({'type':'chunk','content':chunk_content,'timestamp':time.time()}, ensure_ascii=False)}\n\n"

        self.reply_llm_use_time += time.time() - t_reply
        # 生成完整回复后处理日志和返回结果
        full_content = ''.join(content)
        self.reply_llm_use_time = time.time() - t_reply  # 假设这是实例变量
        ret = {
            "type": "final",
            "data": {
                "status": 0,
                "msg": full_content,
                "onChainCalls": self.on_chain_calls,
            },
            'timestamp':time.time()
        }
        logging.info(f"Chat_id={self.chat_id} - Replier llm call finished - msg={full_content}|reply_llm_use_time: {self.reply_llm_use_time} seconds")
        yield f"data: {json.dumps(ret, ensure_ascii=False)}\n\n"
    

    async def _call_tool_caller(self, content):
        content.message.tool_calls = content.message.tool_calls[:MAX_CALL_PER_ROUND]
        for tool_call in content.message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if (tool_name, tool_args) in self.tools_called:
                logging.warning(f"Chat_id={self.chat_id}｜Tool call={tool_name}｜args={tool_args} ALREADY CALLED. ")
                continue
            else:
                self.tools_called.append((tool_name, tool_args))

            # 记录开始时间
            start_ts = time.perf_counter()
            # 执行tool
            result = await self.session.call_tool(tool_name, tool_args)
            # 计算耗时
            elapsed = time.perf_counter() - start_ts
            #  日志里打印
            logging.info(
                f"Chat_id={self.chat_id} | Tool={tool_name} | "
                f"Args={tool_args} | Elapsed={elapsed:.3f}s | Result={result}"
            )
            if tool_name.startswith("onChain"):
                tool_call_content = json.loads(result.content[0].text)
                if tool_call_content not in self.on_chain_calls:
                    self.on_chain_calls.append(tool_call_content)
                    self.messages.append({
                        "role": "assistant",
                        "content": f"I am calling the blockchain method: {tool_call_content}. DO NOT CALL IT AGAIN. ",
                    })
                else:
                    logging.info(f"Chat_id={self.chat_id}｜Tool call={tool_name}｜args={tool_args} ALREADY CALLED. ")
                    self.messages.append({
                        "role": "assistant",
                        "content": f"I MUST recap the information gathered so far and give a final answer now. ",
                    })
                if not self.onChain_tool_called:
                    self.onChain_tool_called = True
                    self.messages.append({
                        "role": "assistant",
                        "content": "Now I need to politely inform the user that I am now calling the blockchain method on their behalf. ",
                    })
            else:
                self.messages.append(content.message.model_dump())
                self.messages.append({
                    "role": "tool",
                    "content": ",".join([i.text for i in result.content]),
                    "tool_call_id": tool_call.id,
                })
        self.tool_call_count += 1
        if self.tool_call_count == MAX_ROUNDS - 1:
            self.messages.append({
                "role": "assistant",
                "content": "Max tool calls reached. Now I MUST give a final answer.",
            })
        
    async def process_query_stream(self, msg: List[Dict[str, str]]) -> AsyncGenerator[Dict[str, Any], None]:
        try:
            t0 = time.time()
            ret = {"status": 1, "msg": "error", "onChainCalls": []}
            logging.info(f"Chat_id: {self.chat_id} - Processing query: {msg}, address: {self.address}")

            self.available_tools = await self.get_available_tools()
            await self.process_messages(msg)

            while self.tool_call_count < MAX_ROUNDS:
                t1 = time.time()
                # call tools model
                logging.info(f"Chat_id={self.chat_id} - Calling tool caller model")
                response = self.client.chat.completions.create(
                    model=os.getenv("LLM_MODEL"),
                    messages=self.messages,
                    tools=self.available_tools,
                )
                content = response.choices[0]
                self.tool_caller_llm_use_time += time.time() - t1

                if content.finish_reason == "tool_calls":
                    await self._call_tool_caller(content)
                else:
                    async for sse_chunk in self._call_replier():
                        yield sse_chunk
                    logging.info(f"Chat_id={self.chat_id} - Answer generated after tool calls - on_chain_calls: {self.on_chain_calls}｜time: {time.time() - t0} seconds｜tool_caller_llm_use_time: {self.tool_caller_llm_use_time} seconds｜reply_llm_use_time: {self.reply_llm_use_time} seconds")
                    return
            logging.info(f"Chat_id={self.chat_id} - No final answer generated after tool calls.")
            async for sse_chunk in self._call_replier():
                yield sse_chunk
            logging.info(f"Chat_id={self.chat_id} - Answer generated after tool calls - on_chain_calls: {self.on_chain_calls}｜time: {time.time() - t0} seconds｜tool_caller_llm_use_time: {self.tool_caller_llm_use_time} seconds｜reply_llm_use_time: {self.reply_llm_use_time} seconds")
            return
        except Exception as e:
            msg = "Error processing query."
            ret = {
                "type": "final",
                "data": {
                    "status": 0,
                    "msg": msg,
                    "onChainCalls": self.on_chain_calls,
                },
            'timestamp':time.time()
            }
            logging.error(f"Chat_id={self.chat_id} - Error processing query - msg={msg}｜on_chain_calls={self.on_chain_calls}｜error={e}｜time={time.time() - t0} seconds｜tool_caller_llm_use_time: {self.tool_caller_llm_use_time} seconds｜reply_llm_use_time: {self.reply_llm_use_time} seconds")
            yield f"data: {json.dumps(ret, ensure_ascii=False)}\n\n"
            return
    
    async def cleanup(self):
        await self.exit_stack.aclose()

@app.post("/query_stream")
async def handle_query_stream(query_request: QueryRequest, background_tasks: BackgroundTasks,):
    client = MCPClient(address=query_request.address, chainid=query_request.chainid)
    await client.connect_to_server()
    msg = [m.model_dump() for m in query_request.msg]
    background_tasks.add_task(client.cleanup)

    return StreamingResponse(
        client.process_query_stream(msg),
        media_type="text/event-stream"
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app,
        http="httptools",
        host="127.0.0.1",
        port=8861,
        log_config=None,
        timeout_keep_alive=10,
        limit_concurrency=10
    )
