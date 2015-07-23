#coding:utf-8
__author__ = 'xp'

class Question:
    def __init__(self, time, ram, question_id, context, name, point, submit_total, accept_total):
        self.__time = int(time)
        self.__ram = int(ram)
        self.__id = int(question_id)
        self.__context = context
        self.__name = name
        self.__point = int(point)
        self.__submitTotal = submit_total
        self.__acceptTotal = accept_total

    def __init__(self, dict):
        self.__id = dict['id']
        self.__name = dict['name']
        self.__ram = dict['ram']
        self.__point = dict['point']
        self.__context = dict['context']
        self.__time = dict['time']
        self.__submitTotal = dict['submitTotal']
        self.__acceptTotal = dict['acceptTotal']

    def get_time(self):
        return self.__time

    def get_ram(self):
        return self.__ram

    def get_id(self):
        return self.__id

    def get_context(self):
        return self.__context

    def get_name(self):
        return self.__name

    def get_point(self):
        return self.__point

    def get_submit_total(self):
        return self.__submitTotal

    def get_accept_total(self):
        return self.__acceptTotal
