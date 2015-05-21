# -*- coding:UTF-8 -*-
__author__ = 'xp'

import time
from threading import Thread

import Submit
import TestData
import Question
import DataBaseLinker
from Log import Log
from PathData import DATA
from DockerRunner import DockerRunner
from Manufacturer import Manufacturer
from ShellCreater import ShellCreater
from AnalysisResult import AnalysisResult
from OJDataBaseAdministrator import OJDataBaseAdministrator as OJDBA

# name, point, ram, context, time, id
# user_id, question_id, submit_time, type, codeName, result
# question_id, test_data, result_data

if __name__ == '__main__':
    Manufacturer.getInstance().getDataFromDB()
    print Manufacturer.getInstance().getQueueHead()