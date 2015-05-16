__author__ = 'xp'

class Log:
    isDebud = True
    isCustomer = True
    isProducer = True
    isCompile = True
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
    def CompileLog(value):
        if Log.isCompile:
            Log.LOG(value)

    @staticmethod
    def AnalysisResultLog(value):
        if Log.isAnalysisResult:
            Log.LOG(value)