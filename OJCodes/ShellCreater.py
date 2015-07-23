# coding:utf-8
__author__ = 'xp'

import os
import time
import random
from Log import Log
from Shell import Shell
from subprocess import *
from PathData import DATA


class ShellCreater:

    @staticmethod
    def createCompileShell(codeName, exeName, compileType):
        Log.CompileLOG('Compile: create compile file')
        shell = Shell(name= 'compile_' + codeName + '_' + exeName + '_' + compileType + '.sh', path=DATA.HOST_SHELL_PATH)
        # 生成编译的sh文件
        compileName = ''
        if compileType.upper() == 'C':
            compileName = 'gcc ' + DATA.DOCKER_CODES_PATH + '/' + codeName + '.c -o ' + DATA.DOCKER_EXES_PATH + '/' + exeName
        elif compileType.upper() == 'CPP':
            compileName = 'g++ ' + DATA.DOCKER_CODES_PATH + '/' + codeName + '.cpp -o ' + DATA.DOCKER_EXES_PATH + '/' + exeName
        elif compileType.upper() == 'JAVA':
            compileName = 'javac ' + DATA.DOCKER_CODES_PATH + '/' + codeName + '.java\n'
            compileName += 'mv ' + DATA.DOCKER_CODES_PATH + '/' + exeName + '.class ' + DATA.DOCKER_EXES_PATH
        elif compileType.upper() == 'PY':
            compileName = 'cp ' + DATA.DOCKER_CODES_PATH + '/' + codeName + '.py ' + DATA.DOCKER_EXES_PATH
        Log.CompileLOG('Compile: Get Compile Name')
        try:
            Log.CompileLOG('Compile: Create file and write data')
            file = open(shell.getPath() + '/' + shell.getName(), 'w')
            file.write("#! /bin/bash\n")
            file.write(compileName + '\n')
            file.write("if [ \"$?\" = \"0\" ]\n")
            file.write("then echo 'success'\nelse\necho 'fail'\nfi")
            file.close()
            Log.CompileLOG('Compile: write data over')
            os.system("chmod 777 " + shell.getPath() + '/' + shell.getName())
        except Exception,e:
            file.close()
            print e.message
            errorLog = file(DATA.HOST_ERROR_LOG_PATH + '/create_compile_shell_' + str(time.time()) + str(random.randint(1000,9999)) + '.log','w')
            errorLog.write(e.message)
            errorLog.close()
            return None
        return shell

    @staticmethod
    def createRunShell(exeName, interpreter, question, param=[]):
        Log.CompileLOG('RUN: create run file')
        scale = 1
        suffix = ''
        interpreterValue = ''
        exeSentence = 'time ('
        if len(param) > 0:
            exeSentence += 'echo '
            for item in param:
                exeSentence += (str(item) + ' ')
            exeSentence += ' | '
        if interpreter.upper() == 'C' or interpreter.upper() == 'CPP':
            interpreterValue = ''
        elif interpreter.upper() == 'PY':
            interpreterValue = 'python'
            scale = 3
            suffix = '.py'
        elif interpreter.upper() == 'JAVA':
            interpreterValue = 'java'
            scale = 2
            suffix = '.java'
        Log.CompileLOG('RUN: Get interpreter value')
        exeSentence += (interpreterValue + ' .' + DATA.DOCKER_EXES_PATH + '/' + exeName + suffix + ' )')
        Log.CompileLOG('RUN: The Exesentence is : '+exeSentence)
        #生成编译的sh文件
        try:
            Log.CompileLOG('RUN: create file and write data')
            shell = Shell(name='run_'+exeName+'_'+interpreter+'.sh', path=DATA.HOST_SHELL_PATH)
            Log.CompileLOG('RUN: ' + shell.getPath() + '/' + shell.getName())
            file = open(shell.getPath() + '/' + shell.getName(), "w")
            file.write('#! /bin/bash\n')
            file.write('ulimit -s -t ' + str(question.getTime() * scale) + '\n')
            file.write(exeSentence + '\n')
            file.close()
            Log.CompileLOG('RUN: write data over')
            Popen("chmod 777 " + shell.getPath() + '/' + shell.getName(),shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
        except Exception,e:
            file.close()
            Log.CompileLOG('RUN: The error is : ' + e.message )
            errorLog = file(DATA.HOST_ERROR_LOG_PATH + '/create_run_shell_' + str(time.time()) + str(random.randint(1000,9999)) + '.log', 'w')
            errorLog.write(e.message)
            errorLog.close()
            return None
        return shell

    @staticmethod
    def removeShell(shell):
        try:
            os.system('rm ' + shell.getPath() + '/' + shell.getName())
        except Exception,e:
            errorLog = file(DATA.HOST_ERROR_LOG_PATH + '/create_run_shell_' + str(time.time()) + str(random.randint(1000,9999)) + '.log', 'w')
            errorLog.write(e.message)
            errorLog.close()
            return False
        return True