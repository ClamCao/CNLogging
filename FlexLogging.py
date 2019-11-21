# -*- coding=utf-8 -*-
# !/usr/bin/python2.7

import datetime
import logging
import os
import warnings


class Logger(object):

    def __init__(self, loggerName='LogJobs', fileHandlerEnable=True, logDirPath="./", streamEnable=False, serious=False):

        self.name = loggerName
        logFilename = "_".join([self.name, datetime.datetime.now().isoformat()[:-3], ]) + ".log"
        self.__logFileAbs = os.path.join(logDirPath, logFilename)

        self._FORMATTER = logging.Formatter(fmt="[%(asctime)15s] %(message)s")

        self.__logger = logging.getLogger(loggerName)
        self.__logger.setLevel(10)

        if fileHandlerEnable not in (False, None, 0):
            self.__fileHandlerEnable = True
            self.__logFilePath = logDirPath
            self.__fileHandler = logging.FileHandler(self.__logFileAbs)
            self.__fileHandler.setFormatter(self._FORMATTER)
            self.__fileHandler.setLevel(10)
        else:
            self.__logFilePath = None
            self.__fileHandler = None
            self.__fileHandlerEnable = False

        if streamEnable not in (False, None, 0):
            self.__consoleHandler = logging.StreamHandler()
            self.__consoleHandler.setFormatter(self._FORMATTER)
            self.__consoleHandler.setLevel(10)
            self.__consoleHandlerEnable = True
        else:
            self.__consoleHandler = None
            self.__consoleHandlerEnable = False

        [self.__logger.addHandler(handler) for handler in [self.__consoleHandler, self.__fileHandler] if handler is not None]

    @property
    def fileHandlerEnable(self):
        return self.__fileHandlerEnable

    @fileHandlerEnable.setter
    def fileHandlerEnable(self, TOF):
        if isinstance(TOF, bool):
            if TOF is True:

                if (self.__fileHandler is not None) and (self.__fileHandler in self.__logger.handlers) and (self.__fileHandlerEnable is True):
                    warnings.warn('[warn] invalid operation, fileHandlerEnable is set True, and FileHandler has been added to handlers.')
                elif self.__fileHandler is None:
                    self.__fileHandler = logging.FileHandler(self.__logFileAbs)
                    self.__fileHandler.setLevel(0)
                    self.__logger.addHandler(self.__fileHandler)
                    self.__fileHandlerEnable = True
                elif self.__fileHandler not in self.__logger.handlers:
                    self.__logger.addHandler(self.__fileHandler)
                    self.__fileHandlerEnable = True

            else:
                if self.__fileHandler is not None:
                    if self.__fileHandler in self.__logger.handlers:
                        self.__logger.handlers.remove(self.__fileHandler)
                        self.__fileHandlerEnable = False
                    else:
                        warnings.warn('[warn] invalid operation, FileHandler was not in handlers.')
        else:
            raise ValueError('parameter type should be <bool>, not <{}>.'.format(type(TOF)))

    @property
    def consoleHandlerEnable(self):
        return self.__consoleHandlerEnable

    @consoleHandlerEnable.setter
    def consoleHandlerEnable(self, TOF):
        if isinstance(TOF, bool):
            if TOF is True:

                if (self.__consoleHandler is not None) and (self.__consoleHandler in self.__logger.handlers) and (self.__consoleHandlerEnable is True):
                    warnings.warn('[warn] invalid operation, consoleHandlerEnable is set True, and consoleHandler has been added to handlers.')
                elif self.__consoleHandler is None:
                    self.__consoleHandler = logging.StreamHandler()
                    self.__consoleHandler.setFormatter(self._FORMATTER)
                    self.__consoleHandler.setLevel(0)
                    self.__logger.addHandler(self.__consoleHandler)
                    self.__consoleHandlerEnable = True
                elif self.__consoleHandler not in self.__logger.handlers:
                    self.__logger.addHandler(self.__consoleHandler)
                    self.__consoleHandlerEnable = True

            else:
                if self.__consoleHandler is not None:
                    if self.__consoleHandler in self.__logger.handlers:
                        self.__logger.handlers.remove(self.__consoleHandler)
                        self.__consoleHandlerEnable = False
                    else:
                        warnings.warn('[warn] invalid operation, consoleHandler was not in handlers.')
        else:
            raise ValueError('parameter type should be <bool>, not <{}>.'.format(type(TOF)))

    def log(self, msg="", where="unknown", ltype="None", extra="None", limited=True):
        if limited:
            self.__logger.debug("[Where]{where:<15} [type] {type:<15} [extra] {extra:<15} [msg] {msg}".format(where=where[:12]+"..." if len(where) > 15 else where, type=ltype[:12]+"..." if len(ltype) > 15 else ltype, msg=msg if len(msg) < 1000 else "...too long...", extra=extra[:12]+"..." if len(extra) > 15 else extra))
        else:
            self.__logger.debug("[Where]{where:<15} [type] {type:<15} [extra] {extra:<15} [msg] {msg}".format(where=where, type=ltype, msg=msg, extra=extra))