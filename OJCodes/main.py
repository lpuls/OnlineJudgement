#coding:utf-8
__author__ = 'xp'

import time
from threading import Thread

import Submit
import TestData
import Question
import DataBaseLinker
from OJDataBaseAdministrator import OJDataBaseAdministrator as OJDBA

#'name', 'point', 'ram', 'context', 'time', id


if __name__ == '__main__':
    pass
    submits = OJDBA.getSubmitWhichWaiting()
    for item in submits:
        print item.getSubmitTime()