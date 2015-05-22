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
from Customer import Customer
from DockerRunner import DockerRunner
from Manufacturer import Manufacturer
from ShellCreater import ShellCreater
from AnalysisResult import AnalysisResult
from OJDataBaseAdministrator import OJDataBaseAdministrator as OJDBA

# QUESTION:  name, point, ram, context, time, id
# SUBMIT:    user_id, question_id, submit_time, type, codeName, result
# TEST DATA: question_id, test_data, result_data

if __name__ == '__main__':
    submitInfo = {'user_id': 'xp', 'question_id': '1', 'submit_time': '2015-06-06 12:23:25', 'type': 'cpp', 'codeName': 'xp_0000_20150606122323_cpp', 'result': 'waiting'}
    submit = Submit.Submit(submitInfo)
    customer = Customer()
    if customer.compile(submit):
        print 'run program'
        question = OJDBA.getQuestion(submit.getQuestionID())
        result = customer.runProgram(submit.getCodeName(), submit.getType(), question, [1, 2])
        print result
        if result is not None:
            print AnalysisResult.analysis(result, [3])
        else:
            print 'Run None Type'
    else:
        print 'Compile None Type'
    print 'OVER'
