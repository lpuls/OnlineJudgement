# coding:utf-8
__author__ = 'xp'



class Submit:
    def __init__(self, user_id, result, submit_time, code_name, language_type, question_id):
        self.__userID = user_id
        self.__result = result
        self.__submitTIme = submit_time
        self.__codeName = code_name
        self.__type = language_type
        self.__questionID = int(question_id)

    def __init__(self, dict):
        self.__userID = dict['user_id']
        self.__result = dict['result']
        self.__submitTIme = dict['submit_time']
        self.__codeName = dict['codeName']
        self.__type = dict['type']
        self.__questionID = dict['question_id']

    def get_user_id(self):
        return self.__userID

    def get_result(self):
        return self.__result

    def get_submit_time(self):
        return self.__submitTIme

    def get_code_name(self):
        return self.__codeName

    def get_language_type(self):
        return self.__type

    def get_question_id(self):
        return self.__questionID


