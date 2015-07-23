# _*_ coding:utf-8 _*_
__author__ = 'xp'

import time
import threading

from Log import Log
from PathData import DATA
from DockerRunner import DockerRunner


class TimeSupervisor:
    def __init__(self, container_id, time_limit=10):
        self.__containerID = container_id
        self.__timeLimit = time_limit
        self.__isTimming = False
        self.__timeTotal = 0
        self.__thread = None

    def reset(self):
        self.__timeTotal = 0

    def timming(self):
        while True:
            if self.__isTimming:
                self.__timeTotal += 1
                if self.__timeTotal > DATA.CONTAINER_LIFETIME:
                    DockerRunner.remove_container(self.__containerID)
                    self.__isTimming = False
            time.sleep(1)

    def stop(self):
        self.__isTimming = False

    def start(self):
        self.__isTimming = True
        if self.__thread is None:
            self.__thread = threading.Thread(target=self.timming)
            self.__thread.start()

    def get_container_id(self):
        return self.__containerID

    def set_container_id(self, container_id):
        self.__containerID = container_id

    def get_time_limit(self):
        return self.__timeLimit

    def set_time_limit(self, time_limit):
        self.__timeLimit = time_limit
