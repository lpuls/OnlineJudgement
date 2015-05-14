__author__ = 'xp'

class Log:
    isDebud = True
    @staticmethod
    def LOG(value):
        if Log.isDebud:
            print value