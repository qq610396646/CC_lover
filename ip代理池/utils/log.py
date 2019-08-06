# utils/log.py
import sys
import logging
from settings import LOG_LEVEL,LOG_FILENAME,LOG_DATEFMT,LOG_FMT

class Logger(object):
    def __init__(self):
        self._logger=logging.getLogger()
        self.formatter=logging.Formatter(fmt=LOG_FMT,datefmt=LOG_DATEFMT)
        #设置输出文件模式
        self._logger.addHandler(self._get_file_handle(LOG_FILENAME))
        #设置输出终端的模式
        self._logger.addHandler(self._get_console_handler())
        #日志等级
        self._logger.setLevel(LOG_LEVEL)

    def _get_file_handle(self, filename):
        #文件日志的handler
        filehandler=logging.FileHandler(filename=filename,encoding="utf-8")
        filehandler.setFormatter(self.formatter)
        return filehandler

    def _get_console_handler(self):
        #获取一个输出到终端的日志handler
        console_handler=logging.StreamHandler(sys.stdout)
        #设置格式
        console_handler.setFormatter(self.formatter)
        return  console_handler
    @property
    def logger(self):
        return self._logger

logger=Logger().logger

if __name__=="__main__":
    logger.debug("调试信息")
    logger.info("状态信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误信息")