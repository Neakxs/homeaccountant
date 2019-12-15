import copy
import enum
import logging
import logging.handlers


class LogLevel(enum.IntEnum):
    NOSET = 0x0
    TRACE = 0x10
    DEBUG = 0x20
    INFO = 0x30
    WARNING = 0x40
    ERROR = 0x50
    CRITICAL = 0x60


class ColoredConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        myrecord = copy.copy(record)
        levelno = myrecord.levelno
        if levelno >= LogLevel.CRITICAL:
            color = '\x1b[35m'
        elif levelno >= LogLevel.ERROR:
            color = '\x1b[31m'
        elif levelno >= LogLevel.WARNING:
            color = '\x1b[33m'
        elif levelno >= LogLevel.INFO:
            color = '\x1b[32m'
        elif levelno >= LogLevel.DEBUG:
            color = '\x1b[36m'
        elif levelno >= LogLevel.TRACE:
            color = '\x1b[34m'
        else:
            color = '\x1b[0m'
        myrecord.msg = color + str(myrecord.msg) + '\x1b[0m'
        logging.StreamHandler.emit(self, myrecord)
