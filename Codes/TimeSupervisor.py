#coding:utf-8
__author__ = 'xp'

import time
import docker

class TimeSupervisor:
    dockerLinker = None
    @staticmethod
    def setDockerLinker(dockerLinker):
        TimeSupervisor.dockerLinker = dockerLinker
    def __init__(self, containerData, timeLimit):
        self.__containerData = containerData
        self.__timeLimit = timeLimit
        self.__timeTotal = 0
    def getContainerData(self):
        return self.__containerData
    def getTimeLimit(self):
        return self.__timeLimit
    def getTimeTotal(self):
        return self.__timeTotal
    def timeAdd(self):
        self.__timeTotal += 1
        if self.__timeTotal >= self.__timeLimit:
            self.reStart()
            return self.killContainer()
        time.sleep()
    def reStart(self):
        self.__timeTotal = 0
    def killContainer(self):
        try:
            TimeSupervisor.dockerLinker.stop(container=self.__containerData['Id'])
            TimeSupervisor.dockerLinker.remove_container(container=self.__containerData['Id'])
        except Exception,e:
            return False
        return True