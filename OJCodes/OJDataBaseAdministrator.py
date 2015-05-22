# coding:utf-8
__author__ = 'xp'

import time

from Submit import Submit
from PathData import DATA
from Question import Question
from TestData import TestData
from DataBaseLinker import DataBaseLinker


class OJDataBaseAdministrator:
    __mutex = True

    @staticmethod
    def waitMutex():
        while True:
            #因数据库不能同时访问，所以只有当数据库信号量为真时，才可进行访问
            if OJDataBaseAdministrator.__mutex:
                OJDataBaseAdministrator.__mutex = False
                break
            time.sleep(0.1)

    @staticmethod
    def releaseMutex():
        OJDataBaseAdministrator.__mutex = True

    @staticmethod
    def updataSubmitRrsult(result, codeName):
        OJDataBaseAdministrator.waitMutex()
        result = DataBaseLinker.getInstance().execute("update Submit set result='" + result + "' where codeName='" + codeName + "'")
        OJDataBaseAdministrator.releaseMutex()
        return result

    @staticmethod
    def getQuestion(id):
        OJDataBaseAdministrator.waitMutex()
        result = DataBaseLinker.getInstance().execute("select * from Question where id='" + str(id) + "'")
        question = Question(result[0])
        OJDataBaseAdministrator.releaseMutex()
        return question

    @staticmethod
    def getSubmitWhichWaiting():
        OJDataBaseAdministrator.waitMutex()
        result = DataBaseLinker.getInstance().execute("select * from Submit where result='waiting'")
        OJDataBaseAdministrator.releaseMutex()
        submits = []
        for item in result:
            submit = Submit(item)
            submits.append(submit)
        return submits

    @staticmethod
    def getTestDataByQuestionID(id):
        OJDataBaseAdministrator.waitMutex()
        result = DataBaseLinker.getInstance().execute("select * from TestData where question_id='" + str(id) + "'")
        OJDataBaseAdministrator.releaseMutex()
        testDatas = []
        for item in result:
            testData = TestData(item)
            testDatas.append(testData)
        return testDatas

    @staticmethod
    def getUserByUserID(id):
        OJDataBaseAdministrator.waitMutex()
        result = DataBaseLinker.getInstance().execute("select * from Users where user_id='" + str(id) + "'")
        OJDataBaseAdministrator.releaseMutex()
        return result

    @staticmethod
    def updateCompilerError(codeName):
        return OJDataBaseAdministrator.updataSubmitRrsult('Compiler Error', codeName)

    @staticmethod
    def updateRunning(codeName):
        return OJDataBaseAdministrator.updataSubmitRrsult('Running', codeName)

    @staticmethod
    def updateMemoryLimitExceeded(codeName):
        return OJDataBaseAdministrator.updataSubmitRrsult('Memory Limit Exceeded', codeName)

    @staticmethod
    def updateTimeLimitExceeded(codeName):
        return OJDataBaseAdministrator.updataSubmitRrsult('Time Limit Exceeded', codeName)

    @staticmethod
    def updateRuntimeError(codeName):
        return OJDataBaseAdministrator.updataSubmitRrsult('Runtime Error', codeName)

    @staticmethod
    def updateWrongAnswer(codeName):
        return OJDataBaseAdministrator.updataSubmitRrsult('Wrong Answer', codeName)

    @staticmethod
    def updateOutputLimitExceeded(codeName):
        return OJDataBaseAdministrator.updataSubmitRrsult('Output Limit Exceeded', codeName)

    @staticmethod
    def updatePresentationError(codeName):
        return OJDataBaseAdministrator.updataSubmitRrsult('Presentation Error', codeName)

    @staticmethod
    def updateAccepted(codeName):
        return OJDataBaseAdministrator.updataSubmitRrsult('Accepted', codeName)

    @staticmethod
    def addQuestion(question):
        OJDataBaseAdministrator.waitMutex()
        result = DataBaseLinker.getInstance().execute("insert into Question (name, context, time, ram, point) value ('" + question.getName() + "', '" + question.getContext() + "',"+str(question.getTime())+","+str(question.getRam())+"," + str(question.getPoint()) + ")")
        OJDataBaseAdministrator.releaseMutex()
        return result

    @staticmethod
    def addSubmit(submit):
        sql = "insert into Submit (user_id, question_id, submit_time, type, codeName, result) value ('"#xp',1,'2015-06-06 12:23:23','cpp','xp_0000_20150606122323_cpp','waiting');"
        sql = sql + submit.getUserID() + "','" + str(submit.getQuestionID()) +"','" + submit.getSubmitTime() + "','" + submit.getType() + "','" + submit.getCodeName() + "','" + submit.getResult() + "')"
        OJDataBaseAdministrator.waitMutex()
        result = DataBaseLinker.getInstance().execute(sql)
        OJDataBaseAdministrator.releaseMutex()
        return result

    @staticmethod
    def addTestData(testData):
        sql = "insert into TestData (question_id, test_data, result_data) value ("#1,'[1,1]','[2]');
        sql = sql + str(testData.getQuestionID()) + ",'" + testData.getTestData() + "','" + testData.getResultData() + "')"
        OJDataBaseAdministrator.waitMutex()
        result = DataBaseLinker.getInstance().execute(sql)
        OJDataBaseAdministrator.releaseMutex()
        return result

    @staticmethod
    def addUser(userID, password, userSchool = "", userName="None Name"):
        sql = "insert into Users (user_id, user_name, user_password, user_school) value ('"#xp','xp','085850','TKK');
        sql = sql + userID + "','" + userName + "','" + password + "','" + userSchool + "')"
        OJDataBaseAdministrator.waitMutex()
        result = DataBaseLinker.getInstance().execute(sql)
        OJDataBaseAdministrator.releaseMutex()
        return result

    @staticmethod
    def updateByResult(result, codeName):
        if result == DATA.COMPILE_ERROR:
            OJDataBaseAdministrator.updateCompilerError(codeName)
        elif result == DATA.MEMORY_LIMIT_EXCEEDED:
            OJDataBaseAdministrator.updateMemoryLimitExceeded(codeName)
        elif result == DATA.TIME_LIMIT_EXCEEDED:
            OJDataBaseAdministrator.updateTimeLimitExceeded(codeName)
        elif result == DATA.WRONG_ANSWER:
            OJDataBaseAdministrator.updateWrongAnswer(codeName)
        elif result == DATA.OUTPUT_LIMIT_EXCEEDED:
            OJDataBaseAdministrator.updateOutputLimitExceeded(codeName)
        elif result == DATA.PRESENTATION_ERROR:
            OJDataBaseAdministrator.updatePresentationError(codeName)
        elif result == DATA.ACCEPT:
            OJDataBaseAdministrator.updateAccepted(codeName)