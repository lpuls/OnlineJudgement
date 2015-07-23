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
    def __init__(self):
        pass

    @staticmethod
    def create_compile_shell(code_name, exe_name, compile_type):
        Log.compile_log('Compile: create compile file')
        shell = Shell(name= 'compile_' + code_name + '_' + exe_name + '_' + compile_type + '.sh',
                      path=DATA.HOST_SHELL_PATH)
        # 生成编译的sh文件
        compile_name = ''
        if compile_type.upper() == 'C':
            compile_name = 'gcc ' + DATA.DOCKER_CODES_PATH + '/' + code_name + '.c -o ' \
                           + DATA.DOCKER_EXES_PATH + '/' + exe_name
        elif compile_type.upper() == 'CPP':
            compile_name = 'g++ ' + DATA.DOCKER_CODES_PATH + '/' + code_name + '.cpp -o ' \
                           + DATA.DOCKER_EXES_PATH + '/' + exe_name
        elif compile_type.upper() == 'JAVA':
            compile_name = 'javac ' + DATA.DOCKER_CODES_PATH + '/' + code_name + '.java\n'
            compile_name += 'mv ' + DATA.DOCKER_CODES_PATH + '/' + exe_name + '.class ' + DATA.DOCKER_EXES_PATH
        elif compile_type.upper() == 'PY':
            compile_name = 'cp ' + DATA.DOCKER_CODES_PATH + '/' + code_name + '.py ' + DATA.DOCKER_EXES_PATH
        Log.compile_log('Compile: Get Compile Name')
        try:
            Log.compile_log('Compile: Create file and write data')
            compile_file = open(shell.get_path() + '/' + shell.get_name(), 'w')
            compile_file.write("#! /bin/bash\n")
            compile_file.write(compile_name + '\n')
            compile_file.write("if [ \"$?\" = \"0\" ]\n")
            compile_file.write("then echo 'success'\nelse\necho 'fail'\nfi")
            compile_file.close()
            Log.compile_log('Compile: write data over')
            os.system("chmod 777 " + shell.get_path() + '/' + shell.get_name())
        except Exception,e:
            compile_file.close()
            print e.message
            error_log = compile_file(DATA.HOST_ERROR_LOG_PATH + '/create_compile_shell_' + str(time.time()) + str(random.randint(1000,9999)) + '.log','w')
            error_log.write(e.message)
            error_log.close()
            return None
        return shell

    @staticmethod
    def create_run_shell(exe_name, interpreter, question, param=[]):
        Log.compile_log('RUN: create run file')
        scale = 1
        suffix = ''
        interpreter_value = ''
        exe_sentence = 'time ('
        if len(param) > 0:
            exe_sentence += 'echo '
            for item in param:
                exe_sentence += (str(item) + ' ')
            exe_sentence += ' | '
        if interpreter.upper() == 'C' or interpreter.upper() == 'CPP':
            interpreter_value = ''
        elif interpreter.upper() == 'PY':
            interpreter_value = 'python'
            scale = 3
            suffix = '.py'
        elif interpreter.upper() == 'JAVA':
            interpreter_value = 'java'
            scale = 2
            suffix = '.java'
        Log.compile_log('RUN: Get interpreter value')
        exe_sentence += (interpreter_value + ' .' + DATA.DOCKER_EXES_PATH + '/' + exe_name + suffix + ' )')
        Log.compile_log('RUN: The Exesentence is : '+exe_sentence)
        # 生成编译的sh文件
        try:
            Log.compile_log('RUN: create file and write data')
            shell = Shell(name='run_'+exe_name+'_'+interpreter+'.sh', path=DATA.HOST_SHELL_PATH)
            Log.compile_log('RUN: ' + shell.get_path() + '/' + shell.get_name())
            run_file = open(shell.get_path() + '/' + shell.get_name(), "w")
            run_file.write('#! /bin/bash\n')
            run_file.write('ulimit -s -t ' + str(question.get_time() * scale) + '\n')
            run_file.write(exe_sentence + '\n')
            run_file.close()
            Log.compile_log('RUN: write data over')
            Popen("chmod 777 " + shell.get_path() + '/' + shell.get_name(),shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
        except Exception, e:
            run_file.close()
            Log.compile_log('RUN: The error is : ' + e.message )
            error_log = run_file(DATA.HOST_ERROR_LOG_PATH + '/create_run_shell_' + str(time.time())
                                 + str(random.randint(1000, 9999)) + '.log', 'w')
            error_log.write(e.message)
            error_log.close()
            return None
        return shell

    @staticmethod
    def remove_shell(shell):
        try:
            os.system('rm ' + shell.get_path() + '/' + shell.get_name())
        except Exception, e:
            error_log = file(DATA.HOST_ERROR_LOG_PATH + '/create_run_shell_' + str(time.time())
                            + str(random.randint(1000, 9999)) + '.log', 'w')
            error_log.write(e.message)
            error_log.close()
            return False
        return True
