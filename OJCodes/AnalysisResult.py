# coding:utf-8
__author__ = 'xp'

import re

from PathData import DATA


class AnalysisResult:

    @staticmethod
    def compileAnalysis(result):
        value = re.compile(r'success',re.X)
        match = value.findall(result)
        if match:
            return True
        else:
            return False

    @staticmethod
    def analysis(result, target):
        if AnalysisResult.isMemoryLimitExceeded(result):
            return DATA.MEMORY_LIMIT_EXCEEDED
        elif AnalysisResult.isTimeOut(result):
            return DATA.TIME_LIMIT_EXCEEDED
        elif AnalysisResult.isWrongAnswer(result, target):
            return DATA.WRONG_ANSWER
        elif AnalysisResult.isOutputLimitExceeded(result, target):
            return DATA.OUTPUT_LIMIT_EXCEEDED
        elif AnalysisResult.isPresentationERror(result, target):
            return DATA.PRESENTATION_ERROR
        else:
            return DATA.ACCEPT

    @staticmethod
    def analysisTime(result):
        time = re.compile(r'sys\s*\d*m\d*.\d*s',re.X)
        match = time.findall(result)
        time = re.compile(r'\d*m\d*.\d*s',re.X)
        sysTime = (time.findall(match[0]))[0]
        result = ''
        for item in sysTime:
            if item == 'm':
                result += '.'
            elif item == '.':
                pass
            elif item == 's':
                result += 'ms'
            else:
                result += item
        return result

    @staticmethod
    def isTimeOut(result):
        # 检测是否是被杀死而终结
        time = re.compile(r'Killed', re.X)
        match = time.findall(result)
        if len(match) != 0:
            return True
        return False

    @staticmethod
    def isWrongAnswer(result, target):
        # 验证输出结果
        for item in target:
            pattern = re.compile("(?<![\S*])" + str(item) + "(?![\S*])", re.M)
            match = pattern.search(result)
            if match is None:
                return True
        return False

    @staticmethod
    def isOutputLimitExceeded(result, target):
        # 验证输出数量
        pattern = re.compile(r'\n', re.X)
        match = pattern.findall(result)
        if len(match) - 5 != len(target):
            return True
        return False

    @staticmethod
    def isMemoryLimitExceeded(result):
        return False

    @staticmethod
    def isPresentationERror(result, target):
        # 验证格式是否出错
        pattern = re.compile(r'\n',re.X)
        match = pattern.split(result)
        for i in range(1, len(target)):
            matchStr = target[i]
            if len(str(matchStr)) != len(match[i]):
                return True
        return False