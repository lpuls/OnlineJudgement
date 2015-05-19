#coding:utf-8
__author__ = 'xp'

import time
from Submit import Submit
from Question import Question
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
        submits = []
        for item in result:
            submit = Submit(item)
            submits.append(submit)
        OJDataBaseAdministrator.releaseMutex()
        return submits