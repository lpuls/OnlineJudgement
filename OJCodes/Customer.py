# _*_ coding:utf-8 _*_
__author__ = 'xp'

import random

from Log import Log
from PathData import DATA
from ShellCreater import ShellCreater
from DockerRunner import DockerRunner
from Manufacturer import Manufacturer
from TimeSuperivsor import TimeSupervisor
from AnalysisResult import AnalysisResult
from OJDataBaseAdministrator import OJDataBaseAdministrator as OJDBA


class Customer:
    def __init__(self):
        self.__timeSupervisor = TimeSupervisor(containerID=None, timeLimit=DATA.CONTAINER_LIFETIME)

    # this function is used to compile the code and return compile result
    def compile(self, submit):
        shell = ShellCreater.createCompileShell(submit.getCodeName(), submit.getCodeName(), submit.getType())
        container = DockerRunner.getInstance().createContainer('COMPILE')
        result = DockerRunner.getInstance().execCommand(container=container, cmd='.' + DATA.DOCKER_SHELL_PATH + '/' + shell.getName())
        DockerRunner.getInstance().removeContainer(container=container)
        if result is not None:
            if AnalysisResult.compileAnalysis(result=result):
                return True
        return False

    # this function is used to calling docker and run the program
    def runProgram(self, exeName, interpreter, question, param=[]):
        shell = ShellCreater.createRunShell(exeName=exeName, interpreter=interpreter, question=question, param=param)
        container = DockerRunner.getInstance().createContainer('RUN')

        # set containerID of __timeSupervisor
        self.__timeSupervisor.setContainerID(containerID=container)

        # run docker and get result of program which running
        # self.__timeSupervisor.reSet()
        # self.__timeSupervisor.start()
        result = DockerRunner.getInstance().execCommand(container=container, cmd='.' + DATA.DOCKER_SHELL_PATH + '/' + shell.getName())
        # self.__timeSupervisor.stop()
        # remove running container which running program
        Log.CustomerLOG('Remove Container')
        DockerRunner.getInstance().removeContainer(container=container)
        Log.CustomerLOG('Remove success')
        # verification result
        return result

    # the function of judgement thread
    def consumption(self):
        submit = Manufacturer.getInstance().getQueueHead()
        if self.compile(submit):
            question = OJDBA.getTestDataByQuestionID(submit.getQuestionID())
            testDatas = OJDBA.getTestDataByQuestionID(submit.getQuestionID())
            testDatasLength = len(testDatas)
            for i in range(0, DATA.JUDGEMENT_TIMES):
                # get a random position and choose a test Data by this position
                testDataPosition = random.randint(0, testDatasLength-1)
                testData = testDatas[testDataPosition]
                testDatas[testDataPosition] = testDatas[testDatasLength-1]
                testDatasLength -= 1
                # run the program and get the result
                result = self.runProgram(submit.getCodeName(), submit.getCodeName(), question, testData.getTestDataByList())
                # access data base and update the submit result
                if result is not None:
                    analysisResult = AnalysisResult.analysis(result, testData.getResultDataByList())
                    if analysisResult != DATA.ACCEPT:
                        OJDBA.updateByResult(analysisResult, submit.getCodeName())
                        break
                else:
                    OJDBA.updateRuntimeError(submit.getCodeName())
        else:
            OJDBA.updateCompilerError(submit.getCodeName())