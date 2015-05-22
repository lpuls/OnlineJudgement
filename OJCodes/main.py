# -*- coding:UTF-8 -*-
__author__ = 'xp'

import time
from threading import Thread

import Submit
import TestData
import Question
import OJRunner
import DataBaseLinker
from Log import Log
from PathData import DATA
from Customer import Customer
from DockerRunner import DockerRunner
from Manufacturer import Manufacturer
from ShellCreater import ShellCreater
from AnalysisResult import AnalysisResult
from OJDataBaseAdministrator import OJDataBaseAdministrator as OJDBA

# QUESTION:  name, point, ram, context, time, id
# SUBMIT:    user_id, question_id, submit_time, type, codeName, result
# TEST DATA: question_id, test_data, result_data

string = """stack size              (kbytes, -s) 8192
1

real	0m0.002s
user	0m0.000s
sys	0m0.003s

"""

if __name__ == '__main__':
    # print AnalysisResult.analysis(string, [3])

     oj = OJRunner.OJRunner()
     oj.startJudgement()

