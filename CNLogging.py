# -*- coding=utf-8 -*-
# !/usr/bin/python2.7
import datetime
import logging
import os
import sys
import threading


class Observer(object):

    def __init__(self, value=None, callbacks=None):
        if callbacks is None:
            callbacks = []
        self._prisoner = value
        self._observers = callbacks

    @property
    def monitored(self, ):
        return self._prisoner

    @monitored.setter
    def monitored(self, value):
        self._prisoner = value
        for callback in self._observers:
            if isinstance(self._prisoner, dict):
                callback(**self._prisoner)
            elif isinstance(self._prisoner, (tuple, list)):
                callback(*self._prisoner)
            else:
                callback(self._prisoner)

    def bindObserver(self, callback):
        self._observers.append(callback)


LOCKER = threading.RLock()
TIME_FORMAT = "[%Y/%m/%d %H:%M:%S]"
ACTIONS = {'DEBUG', 'INFO', 'WARNING', 'ERROR', }


class LogBase(object):

    _fhdlr = None
    _stdhlr = sys.stdout
    _actions = ACTIONS
    _timeFmt = TIME_FORMAT

    def __init__(self):
        self._locker = LOCKER


class CNLogger(LogBase):

    def __init__(self, loggername=None):
        # type(str) -> None
        super(CNLogger, self).__init__()
        self.loggername = loggername

    def _smartSerialize(self, data):
        # type(str/list/dict) -> str
        if isinstance(data, dict):
            dictContent = "".join("".join(["'", k, "':", self._smartSerialize(v), ","]) for k, v in sorted(data.iteritems(), key=lambda x: x[0]))
            return "".join(["{", dictContent, "}"])
        elif isinstance(data, set):
            setStr = ",".join([self._smartSerialize(i) for i in data])
            return "".join(["{", setStr, "}"])
        elif isinstance(data, list):
            setStr = ",".join([self._smartSerialize(i) for i in data])
            return "".join(["[", setStr, "]"])
        elif isinstance(data, tuple):
            setStr = ",".join([self._smartSerialize(i) for i in data])
            return "".join(["(", setStr, ")"])
        elif isinstance(data, (float, int)):
            return str(data)
        elif isinstance(data, str):
            if data:
                return "".join(["'", data, "'"])
            else:
                return "''"
        elif isinstance(data, unicode):
            return "".join(["'", data.encode('utf8'), "'"])
        else:
            return "".join(["'", str(data), "'"])

    def _genRecord(self, func="", action="", **kwargs):
        # type(str, str, **Kwargs) -> None
        func = "[%20s" % func + "]"
        action = "[%10s" % action + "]"
        kwargs = self._smartSerialize(kwargs) if kwargs else ""
        now = datetime.datetime.now().strftime(self._timeFmt)
        info = "".join([now, func, action, kwargs, "\n"])
        return info

    def log(self, where, action, **kwargs):
        # type(str, str, **kwargs) -> None
        if action in self._actions:
            record = self._genRecord(where, action, **kwargs)
            with self._locker:
                if self._fhdlr:
                    self._fhdlr.write(record)
                    self._fhdlr.flush()
                if self._stdhlr:
                    self._stdhlr.write(record)
                    self._stdhlr.flush()


def logConf(*args, **kwargs):
    # type(*args, **kwargs) -> None
    filename = kwargs.get('filename', None)
    timefmt = kwargs.get('timefmt', None)
    actions = kwargs.get('actions', None)
    stdout = kwargs.get('stdout', None)

    if filename:
        LogBase._fhdlr = open(filename, 'w')
    if timefmt:
        LogBase._timeFmt = timefmt
    if actions:
        LogBase._actions = actions
    if stdout:
        LogBase._stdhlr = sys.stdout
    else:
        LogBase._stdhlr = None


OBR = Observer(callbacks=[logConf])


class CNLogManager(object):
    def __init__(self):
        self.loggerMap = {}

    def newLogger(self, loggername):
        newLogger = CNLogger(loggername)
        with LOCKER:
            self.loggerMap[loggername] = newLogger
        return newLogger


manager = CNLogManager()


def getCNLogger(loggname='default'):
    # type(str) -> CNLogManger obj
    if loggname in manager.loggerMap:
        return manager.loggerMap.get(loggname)
    else:
        return manager.newLogger(loggname)


def basicCNLogging(**kwargs):
    # type(**kwargs) -> None
    OBR.monitored = kwargs