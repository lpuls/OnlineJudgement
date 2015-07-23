# coding:utf-8
__author__ = 'xp'

import json

class TestData:
    def __init__(self, question_id, test_data, result_data):
        self.__questionID = int(question_id)
        self.__testData = test_data
        self.__resultData = result_data

    def __init__(self, dict):
        self.__questionID = dict['question_id']
        self.__testData = dict['test_data']
        self.__resultData = dict['result_data']

    def get_question_id(self):
        return self.__questionID

    def get_test_data(self):
        return self.__testData

    def get_result_data(self):
        return self.__resultData

    def get_test_data_by_list(self):
        # stdData = json.dumps(self.__testData)
        test_data_list = json.loads(self.__testData)
        return test_data_list

    def get_result_data_by_list(self):
        # stdData = json.dumps(self.__resultData)
        result_data_list = json.loads(self.__resultData)
        return result_data_list
