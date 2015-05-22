# coding:utf-8
__author__ = 'xp'

import re

from PathData import DATA
from Log import Log


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
        Log.AnalysisResultLOG('ANALYSIS : 0')
        if AnalysisResult.isMemoryLimitExceeded(result):
            return DATA.MEMORY_LIMIT_EXCEEDED
        Log.AnalysisResultLOG('ANALYSIS : 1')
        if AnalysisResult.isTimeOut(result):
            return DATA.TIME_LIMIT_EXCEEDED
        Log.AnalysisResultLOG('ANALYSIS : 2')
        if AnalysisResult.isWrongAnswer(result, target):
            return DATA.WRONG_ANSWER
        Log.AnalysisResultLOG('ANALYSIS : 3')
        if AnalysisResult.isOutputLimitExceeded(result, target):
            return DATA.OUTPUT_LIMIT_EXCEEDED
        Log.AnalysisResultLOG('ANALYSIS : 4')
        if AnalysisResult.isPresentationERror(result, target):
            return DATA.PRESENTATION_ERROR
        Log.AnalysisResultLOG('ANALYSIS : 5')
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
            # here is a bug!!!
            pattern = re.compile(r'(?<![\S*])' + str(item) + r'(?![\S*])', re.X)
            Log.AnalysisResultLOG('ANALYSIS : the item in target is ' + str(item))
            #pattern = re.compile(str(item), re.X)
            match = pattern.search(result)
            if match is None:
                return True
        return False

    @staticmethod
    def isOutputLimitExceeded(result, target):
        # 验证输出数量
        pattern = re.compile(r'\n', re.X)
        match = pattern.findall(result)
        Log.AnalysisResultLOG('ANALYSIS : this length of match is ' + str(len(match)))
        Log.AnalysisResultLOG('ANALYSIS : this length of target is ' + str(len(target)))
        if len(match) - 5 != len(target):
            return True
        return False

    @staticmethod
    def isMemoryLimitExceeded(result):
        return False

    @staticmethod
    def isPresentationERror(result, target):
        # 验证格式是否出错
        pattern = re.compile(r'\n', re.X)
        match = pattern.split(result)
        for i in range(1, len(target)):
            matchStr = target[i]
            if len(str(matchStr)) != len(match[i]):
                return True
        return False