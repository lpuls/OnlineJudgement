#coding:utf-8
__author__ = 'xp'

import json

class TestData:
    def __init__(self, questionID, testData, resultData):
        self.__questionID = int(questionID)
        self.__testData = testData
        self.__resultData = resultData

    def getQuestionID(self):
        return self.__questionID

    def getTestData(self):
        return self.__testData

    def getResultData(self):
        return self.__resultData

    def getTestDataByList(self):
        stdData = json.dumps(self.__testData)
        testDataList = json.loads(stdData)
        return testDataList

    def getResultDataByList(self):
        stdData = json.dumps(self.__resultData)
        resultDataList = json.loads(stdData)
        return resultDataList
