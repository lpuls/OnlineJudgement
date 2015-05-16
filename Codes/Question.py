#coding:utf-8
__author__ = 'xp'


class Question:
    def __init__(self, time, ram, id, context, name):
        """
        :param time:
        :param ram:
        :param id:
        :param context:
        :param name:
        :return:
        """
        self.__time = int(time)
        self.__ram = int(ram)
        self.__id = id
        self.__context = context
        self.__name = name
    def getTime(self):
        return self.__time
    def getRam(self):
        return self.__ram
    def getId(self):
        return self.__id
    def getContext(self):
        return self.__context
    def getName(self):
        return self.__name