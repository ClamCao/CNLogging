# -*- coding=utf-8 -*-
# !/usr/bin/python2.7
__author__ = 'sinchan'

import datetime
import sys
import threading


LOCKER = threading.RLock()
TIME_FORMAT = "[%Y/%m/%d %H:%M:%S]"
ACTIONS = {'DEBUG', 'INFO', 'WARNING', 'ERROR',}


class LogC(object):

    logfile = None
    stdout = True
    timeFmt = TIME_FORMAT
    actions = ACTIONS

    def __init__(self):
        self._locker = LOCKER


class CNLogger(LogC):

    def __init__(self, loggername=None):
        super(CNLogger, self).__init__()

        self.loggername = loggername

        if self.logfile:
            self.__fhdlr = open(self.logfile, 'a')
        else:
            self.__fhdlr = None

        if self.stdout:
            self.__stdhlr = sys.stdout
        else:
            self.__stdhlr = None

    def _smartSerialize(self, data):
        if isinstance(data, dict):
            dictStr = "{"
            for k, v in data.iteritems():
                dictStr += "'" + k + "':" + self._smartSerialize(v) + ","
            dictStr += "}"
            return dictStr
        elif isinstance(data, (set, list, tuple)):
            setStr = "["
            for i in data:
                setStr += self._smartSerialize(i) + ","
            setStr += "]"
            return setStr
        elif isinstance(data, (float, int)):
            return str(data)
        elif isinstance(data, str):
            if data:
                return "'" + data + "'"
            else:
                return ""
        elif isinstance(data, unicode):
            return "'" + data.encode('utf8') + "'"
        else:
            return "'" + str(data) + "'"

    def _genRecord(self, func="", action="", **kwargs):
        func = "[%20s" % func + "]"
        action = "[%10s" % action + "]"
        kwargs = "" or self._smartSerialize(kwargs)
        now = datetime.datetime.now().strftime(self.timeFmt)
        info = now + func + action + kwargs + "\n"
        return info

    def log(self, where, action, **kwargs):
        if action in self.actions:
            record = self._genRecord(where, action, **kwargs)
            with self._locker:
                if self.__fhdlr:
                    self.__fhdlr.write(record)
                    self.__fhdlr.flush()
                if self.__stdhlr:
                    self.__stdhlr.write(record)
                    self.__stdhlr.flush()


class CNLogManager(object):
    def __init__(self):
        self.loggerMap = {}

    def newLogger(self, loggername):
        newLogger = CNLogger(loggername)
        with LOCKER:
            self.loggerMap[loggername] = newLogger
        return newLogger


manager = CNLogManager()
cnc = LogC


def getCNLogger(loggname='default'):
    if loggname in manager.loggerMap:
        return manager.loggerMap.get(loggname)
    else:
        return manager.newLogger(loggname)


def basicCNLogging(**kwargs):
    filename = kwargs.get('filename', None)
    timefmt = kwargs.get('timefmt', None)
    actions = kwargs.get('actions', None)
    stdout = kwargs.get('stdout', None)

    if filename is not None:
        cnc.logfile = filename
        if stdout is None:
            cnc.stdout = False
        else:
            cnc.stdout = stdout
    if timefmt is not None:
        cnc.timeFmt = timefmt
    if actions is not None:
        cnc.actions = actions