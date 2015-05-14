__author__ = 'xp'

class Submit:
    def __init__(self, userID, result, submitTime, codeName, type,questionID):
        self.__userID = userID
        self.__result = result
        self.__submitTime = str(submitTime)
        self.__codeName = codeName
        self.__type = type
        self.__questionID = questionID
    def getUserID(self):
        return self.__userID
    def getResult(self):
        return self.__result
    def getSubmitTIme(self):
        return self.__submitTime
    def getCodeName(self):
        return self.__codeName
    def getType(self):
        return self.__type
    def getQuestionID(self):
        return self.__questionID