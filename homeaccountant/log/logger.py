import copy
import logging
import logging.handlers

from multiprocessing import Queue

from homeaccountant import config
from homeaccountant.log.utils import ColoredConsoleHandler, LogLevel


class CustomLogger(logging.Logger):
    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(LogLevel.TRACE):
            self._log(LogLevel.TRACE, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(LogLevel.DEBUG):
            self._log(LogLevel.DEBUG, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(LogLevel.INFO):
            self._log(LogLevel.INFO, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(LogLevel.WARNING):
            self._log(LogLevel.WARNING, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(LogLevel.ERROR):
            self._log(LogLevel.ERROR, msg, args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(LogLevel.CRITICAL):
            self._log(LogLevel.CRITICAL, msg, args, **kwargs)


class CustomFormatter(logging.Formatter):
    @classmethod
    def get_formatter(cls, level):
        if level < LogLevel.DEBUG:
            return cls('[%(asctime)s] [%(name)s:%(lineno)s] %(message)s', '%d-%m %H:%M:%S')
        elif level < LogLevel.INFO:
            return cls('[%(asctime)s] [%(name)s] %(message)s', '%d-%m %H:%M:%S')
        else:
            return cls('[%(asctime)s] %(message)s', '%d-%m %H:%M:%S')


logging.setLoggerClass(CustomLogger)


class LogWrapper:
    def __init__(self, level):
        self.__queue = Queue()
        self.__qhandler = logging.handlers.QueueHandler(self.__queue)
        self.__qlistener = logging.handlers.QueueListener(
            self.__queue, *self._get_handlers(level), respect_handler_level=True)
        self.__logger = logging.getLogger('homeaccountant')
        self.__logger.setLevel(level)
        self.__logger.addHandler(self.__qhandler)

    def get_logger(self, name=None):
        if name:
            return self.__logger.getChild(name)
        else:
            return self.__logger

    def start(self):
        self.__qlistener.start()

    def stop(self):
        self.__qlistener.stop()

    def _get_handlers(self, level):
        formatter = CustomFormatter.get_formatter(level)
        if config.SERVER.LOGGING.FILE:
            handler = None
        else:
            handler = ColoredConsoleHandler()
            handler.setLevel(level)
            handler.setFormatter(formatter)
        return [handler]


try:
    log_wrapper = LogWrapper(LogLevel[config.SERVER.LOGGING.VERBOSITY])
except:
    log_wrapper = LogWrapper(LogLevel.INFO)


def getLogger(name=None):
    return log_wrapper.get_logger(name)
