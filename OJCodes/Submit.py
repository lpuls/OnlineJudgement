#coding:utf-8
__author__ = 'xp'



class Submit:
    def __init__(self,userID, result, submitTIme, codeName, type, questionID):
        self.__userID = userID
        self.__result = result
        self.__submitTIme = submitTIme
        self.__codeName = codeName
        self.__type = type
        self.__questionID = int(questionID)

    def __init__(self, dict):
        self.__userID = dict['user_id']
        self.__result = dict['result']
        self.__submitTIme = dict['submit_time']
        self.__codeName = dict['codeName']
        self.__type = dict['type']
        self.__questionID = dict['question_id']

    def getUserID(self):
        return self.__userID

    def getResult(self):
        return self.__result

    def getSubmitTime(self):
        return self.__submitTIme

    def getCodeName(self):
        return self.__codeName

    def getType(self):
        return self.__type

    def getQuestionID(self):
        return self.__questionID


