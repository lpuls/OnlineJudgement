# coding:utf-8
__author__ = 'xp'

import re

from PathData import DATA
from Log import Log


class AnalysisResult:
    def __init__(self):
        pass

    @staticmethod
    def compile_analysis(result):
        value = re.compile(r'success', re.X)
        match = value.findall(result)
        if match:
            return True
        else:
            return False

    @staticmethod
    def analysis(result, target):
        Log.analysis_result_log('ANALYSIS : 0')
        if AnalysisResult.is_memory_limit_exceeded(result):
            return DATA.MEMORY_LIMIT_EXCEEDED
        Log.analysis_result_log('ANALYSIS : 1')
        if AnalysisResult.is_time_out(result):
            return DATA.TIME_LIMIT_EXCEEDED
        Log.analysis_result_log('ANALYSIS : 2')
        if AnalysisResult.is_wrong_answer(result, target):
            return DATA.WRONG_ANSWER
        Log.analysis_result_log('ANALYSIS : 3')
        if AnalysisResult.is_output_limit_exceeded(result, target):
            return DATA.OUTPUT_LIMIT_EXCEEDED
        Log.analysis_result_log('ANALYSIS : 4')
        if AnalysisResult.is_presentation_error(result, target):
            return DATA.PRESENTATION_ERROR
        Log.analysis_result_log('ANALYSIS : 5')
        return DATA.ACCEPT

    @staticmethod
    def analysis_time(result):
        time = re.compile(r'sys\s*\d*m\d*.\d*s',re.X)
        match = time.findall(result)
        time = re.compile(r'\d*m\d*.\d*s',re.X)
        sys_time = (time.findall(match[0]))[0]
        result = ''
        for item in sys_time:
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
    def is_time_out(result):
        # 检测是否是被杀死而终结
        time = re.compile(r'Killed', re.X)
        match = time.findall(result)
        if len(match) != 0:
            return True
        return False

    @staticmethod
    def is_wrong_answer(result, target):
        # 验证输出结果
        for item in target:
            # here is a bug!!!
            pattern = re.compile(r'(?<![\S*])' + str(item) + r'(?![\S*])', re.X)
            Log.analysis_result_log('ANALYSIS : the item in target is ' + str(item))
            # pattern = re.compile(str(item), re.X)
            match = pattern.search(result)
            if match is None:
                return True
        return False

    @staticmethod
    def is_output_limit_exceeded(result, target):
        # 验证输出数量
        pattern = re.compile(r'\n', re.X)
        match = pattern.findall(result)
        Log.analysis_result_log('ANALYSIS : this length of match is ' + str(len(match)))
        Log.analysis_result_log('ANALYSIS : this length of target is ' + str(len(target)))
        if len(match) - 5 != len(target):
            return True
        return False

    @staticmethod
    def is_memory_limit_exceeded(result):
        return False

    @staticmethod
    def is_presentation_error(result, target):
        # 验证格式是否出错
        pattern = re.compile(r'\n', re.X)
        match = pattern.split(result)
        for i in range(1, len(target)):
            match_str = target[i]
            if len(str(match_str)) != len(match[i]):
                return True
        return False
