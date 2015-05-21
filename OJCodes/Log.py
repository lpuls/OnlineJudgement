#coding:utf-8
__author__ = 'xp'

class Log:
    isDebug = True
    isCustomer = True
    isCompile = True
    isProducer = True
    isAnalysisResult = True

    @staticmethod
    def LOG(value):
        if Log.isDebud:
            print value

    @staticmethod
    def CustomerLOG(value):
        if Log.isCustomer :
            Log.LOG(value)

    @staticmethod
    def ProducerLOG(value):
        if Log.isProducer:
            Log.LOG(value)

    @staticmethod
    def CompileLOG(value):
        if Log.isCompile:
            Log.LOG(value)

    @staticmethod
    def AnalysisResultLOG(value):
        if Log.isAnalysisResult:
            Log.LOG(value)