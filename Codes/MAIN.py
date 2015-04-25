#coding:utf-8
#/usr/bin/env python
__author__ = 'xp'

from OJRunner import OJRunner
from DataBase import DataBaseLinker

if __name__ == '__main__':
    #OJRunner.produce()
    OJRunner.running()
    #print DataBaseLinker.getInstance().execute("select * from Submit")
    #OJRunner.compile('myCode','myCode','cpp')
    #OJRunner.runContainer('myCode','cpp',[10,20])
    #OJRunner.analysisREsult("30\nreal    0m0.003s\nuser    0m0.003s\nsys     0m0.001s\n", {'answer':['30'],'sys':1000})