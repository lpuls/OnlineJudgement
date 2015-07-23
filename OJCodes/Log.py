# coding:utf-8
__author__ = 'xp'

class Log:
    isDebug = True
    isCustomer = True
    isCompile = True
    isProducer = True
    isAnalysisResult = True

    def __init__(self):
        pass

    @staticmethod
    def LOG(value):
        if Log.isDebug:
            print value

    @staticmethod
    def customer_log(value):
        if Log.isCustomer:
            Log.LOG(value)

    @staticmethod
    def producer_log(value):
        if Log.isProducer:
            Log.LOG(value)

    @staticmethod
    def compile_log(value):
        if Log.isCompile:
            Log.LOG(value)

    @staticmethod
    def analysis_result_log(value):
        if Log.isAnalysisResult:
            Log.LOG(value)
