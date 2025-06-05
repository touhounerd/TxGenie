import logging
import os
from logging import handlers

BASIC_FORMAT = "%(asctime)s - %(process)d - %(threadName)s - %(thread)d - %(filename)s - [line:%(lineno)d] - %(levelname)s: %(message)s"
#DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
FILE_PATH = './logs/'  # save path
CONSOLE_OUTPUT_LEVEL = logging.INFO  # console output level
FILE_OUTPUT_LEVEL = logging.INFO  # file output level


class Logger(object):

    def __init__(self, logger_name='log'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        self.log_file_name = logger_name + ".log"  # log file name
        # self.log_file_name = logger_name  # log file name
        # log output level
        self.console_output_level = CONSOLE_OUTPUT_LEVEL
        self.file_output_level = FILE_OUTPUT_LEVEL
        # log output format
        self.formatter = logging.Formatter(BASIC_FORMAT)  #, DATE_FORMAT)

    def get_logger(self):
        """add log handler to logger and return, if logger has handler, return directly"""
        if not self.logger.handlers:  # avoid duplicate log
            # console output control
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # split log by time
            # when can be set to:
            #     S second
            #     M minute
            #     H hour
            #     D day
            #     W week (interval==0 means Monday)
            #     MIDNIGHT split log after midnight
            if os.name == 'nt':
                rh = handlers.TimedRotatingFileHandler(os.path.join('log', self.log_file_name), when='MIDNIGHT', interval=1, backupCount=7,encoding='utf-8')
            else:
                rh = handlers.TimedRotatingFileHandler(FILE_PATH+self.log_file_name, when='MIDNIGHT', interval=1, backupCount=7)
            rh.setLevel(self.file_output_level)
            # suffix fixed format: %Y-%m-%d_%H-%M-%S, according to when setting
            # if write other format, the old file will not be deleted, can be seen in the TimedRotatingFileHandler source code
            rh.suffix = "%Y-%m-%d.log"
            rh.setFormatter(self.formatter)
            self.logger.addHandler(rh)
        return self.logger


if __name__ == "__main__":
    logging = Logger("test").get_logger()
    logging.error("this is error information")
