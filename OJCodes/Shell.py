# coding:utf-8
__author__ = 'xp'


class Shell:
    def __init__(self, name, path):
        self.__name = name
        self.__path = path

    def get_name(self):
        return self.__name

    def get_path(self):
        return self.__path
