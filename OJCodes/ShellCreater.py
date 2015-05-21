# coding:utf-8
__author__ = 'xp'

import os
import time
import random
from Shell import Shell
from subprocess import *
from PathData import DATA


class ShellCreater:

    @staticmethod
    def createCompileShell(codeName, exeName, compileType):
        #shell = ShellCreater.createShellFile(name = 'compile_' + codeName + '_' + exeName + '_' + compileType + '.sh', path=DATA.HOST_SHELL_PATH)
        shell = Shell(name= 'compile_' + codeName + '_' + exeName + '_' + compileType + '.sh', path=DATA.HOST_SHELL_PATH)
        #生成编译的sh文件
        compileName = ''
        if compileType.upper() == 'C':
            compileName = 'gcc ' + DATA.DOCKER_CODES_PATH + '/' + codeName  + '.c -o ' + DATA.DOCKER_EXES_PATH + '/' + exeName
        elif compileType.upper() == 'CPP':
            compileName = 'g++ ' + DATA.DOCKER_CODES_PATH + '/' + codeName + '.cpp -o ' + DATA.DOCKER_EXES_PATH + '/' + exeName
        elif compileType.upper() == 'JAVA':
            compileName = 'javac ' + DATA.DOCKER_CODES_PATH + '/' + codeName + '.java\n'
            compileName += 'mv ' + DATA.DOCKER_CODES_PATH + '/' + exeName + '.class ' + DATA.DOCKER_EXES_PATH
        elif compileType.upper() == 'PYTHON':
            compileName = 'cp ' + DATA.DOCKER_CODES_PATH + '/' + codeName + '.py ' + DATA.DOCKER_EXES_PATH
        try:
            print shell.getPath()
            file = open(shell.getPath() + '/' + shell.getName(), 'w')
            file.write("#! /bin/bash\n")
            file.write(compileName + '\n')
            file.write("if [ \"$?\" = \"0\" ]\n")
            file.write("then echo 'success'\nelse\necho 'fail'\nfi")
            file.close()
            os.system("chmod 777 " + shell.getPath() + '/' + shell.getName())
        except Exception,e:
            file.close()
            errorLog = file(DATA.HOST_ERROR_LOG_PATH + '/create_compile_shell_' + str(time.time()) + str(random.randint(1000,9999)) + '.log','w')
            errorLog.write(e.message)
            errorLog.close()
            return None
        return shell

    @staticmethod
    def createRunShell(exeName, interpreter, question, param=[]):
        exeSentence = 'time ('
        if len(param) > 0:
            exeSentence += 'echo '
            for item in param:
                exeSentence += (str(item) + ' ')
            exeSentence += ' | '
        if interpreter.upper() == 'C' or interpreter.upper() == 'CPP':
            interpreterValue = ''
        exeSentence += (interpreterValue + ' .' + DATA.DOCKER_EXES_PATH + '/' + exeName + ' )')
        #生成编译的sh文件
        try:
            shell = Shell(name='run_'+exeName+'_'+interpreter+'.sh', path=DATA.HOST_SHELL_PATH)
            file = open(shell.getPath() + '/' + shell.getName(), "w")
            file.write('#! /bin/bash\n')
            file.write('ulimit -s -t ' + str(question.getTime()) + '\n')
            file.write(exeSentence + '\n')
            file.close()
            Popen("chmod 777 " + shell.getPath() + '/' + shell.getName(),shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
        except Exception,e:
            file.close()
            errorLog = file(DATA.HOST_ERROR_LOG_PATH + '/create_run_shell_' + str(time.time()) + str(random.randint(1000,9999)) + '.log','w')
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