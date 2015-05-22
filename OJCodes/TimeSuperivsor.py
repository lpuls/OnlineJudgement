# _*_ coding:utf-8 _*_
__author__ = 'xp'

import time
import threading

from Log import Log
from PathData import DATA
from DockerRunner import DockerRunner


class TimeSupervisor:
    def __init__(self, containerID, timeLimit = 10):
        self.__containerID = containerID
        self.__timeLimit = timeLimit
        self.__isTimming = False
        self.__timeTotal = 0
        self.__thread = None

    def reSet(self):
        self.__timeTotal = 0

    def timming(self):
        while True:
            if self.__isTimming:
                self.__timeTotal += 1
                if self.__timeTotal > DATA.CONTAINER_LIFETIME:
                    DockerRunner.removeContainer(self.__containerID)
                    self.__isTimming = False
            time.sleep(1)

    def stop(self):
        self.__isTimming = False

    def start(self):
        self.__isTimming = True
        if self.__thread == None:
            self.__thread = threading.Thread(target=self.timming)
            self.__thread.start()

    def getContainerID(self):
        return self.__containerID

    def setContainerID(self, containerID):
        self.__containerID = containerID

    def getTimeLimit(self):
        return self.__timeLimit

    def setTimeLimit(self, timeLimit):
        self.__timeLimit = timeLimit
