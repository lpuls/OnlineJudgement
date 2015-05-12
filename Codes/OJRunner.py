#coding:utf-8
#!/usr/bin/env python
__author__ = 'xp'

import re
import time
import json
import random
import DataBase
import datetime
import threading
from subprocess import *
from PathData import DATA
from DockerRunner import DockerRunner

class OJRunner:
    """
    @:var queue: 存放待测代码的队列
    @:var mutex: 进程同步的标识
    @:var customerMuxter: 消费者之间，在读取OJRunner.queue时的信号量
    @:var threadTime : 记录每个线程开启运行容器的时间
    @:var threads : 存放每个线程的列表
    @:var running: 主运算，在大循中不断地获取待评测数据并评测
        @:param : None
        @:return : None
    @:var compile ：  生成编译用sh，并运行容器对指定代码进行编译
        @:param
        @:return
    @:var __createCompileShellFIle:
        @:param
        @:return
    @:var runContainer:
        @:param
        @:return
    @:var analysisResult:
        @:param
        @:return
    @:var produce
        @:param
        @:return
    @:var waitingDataBase:
        @:param
        @:return
    @:var customer
        @:param
        @:return
    @:var timeSupervisor
        @:param
        @:return
    """
    queue = []
    mutex = True
    customerMuxter = True
    databaseMuxter = True
    threadTime = []
    threads = []

    @staticmethod
    def running():
        #生成从数据库中取出待评测项的线程
        produceThread = threading.Thread(target=OJRunner.produce)
        produceThread.start()
        #开启监视每个容器开启时间的线程
        timeSupervisorThread = threading.Thread(target=OJRunner.timeSupervisor)
        timeSupervisorThread.start()
        #开启评测线程
        for i in range(0, DATA.THREAD_TOTAL):
            customer = threading.Thread(target=OJRunner.customer, args=(i,))
            customer.start()
            OJRunner.threads.append(customer)

    @staticmethod
    def compile(codeName, exeName, compileType):
        """
        :param codeName: 要被编译的代码名
        :param exeName: 要被执行的可执行文件名
        :param compileType: 选择的编译器类型
        :return:
        """
        #当shell语句成功实现才返回真，否则返回值，不进以后续操作
        fileName = 'compile_' + codeName + '_' + exeName + '_' + compileType + '.sh'
        print fileName
        if not OJRunner.__createCompileShellFile(codeName,exeName,compileType):
            Popen('rm ' + DATA.HOST_SHELL_PATH + '/' + fileName,shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
            return False
        result = DockerRunner.runCompile(fileName)
        print 'Create Exe'
        Popen('rm ' + DATA.HOST_SHELL_PATH + '/' + fileName,shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
        print result
        if len(result) != 2:
            return False
        return True

    @staticmethod
    def __createCompileShellFile(codeName, exeName, compileType):
        """
        :param codeName: 要被编译的代码名，只要写文件名，不用后缀
        :param exeName: 要被执行的可执行文件名，只要写文件名，不要用缀
        :param compileType: 选择的编译器类型（c,cpp,java,python）
        :return:
        """

        #选择编译器类型，若是python则要将代码从代码文件夹移动至可执行文件夹，若是JAVA则要在编译后，从代码文件夹剪切。CLASS文件到可移行文件夹
        #文件名由comepile_codeName_exeName_compileType.sh,其中，codeName中包括了用户ID，题目编号和日期，保证不重复
        compileName = ''
        if compileType == 'c':
            compileName = 'gcc ' + DATA.DOCKER_CODES_PATH + '/' + codeName  + '.c -o ' + DATA.DOCKER_EXES_PATH + '/' + exeName
        elif compileType == 'cpp':
            compileName = 'g++ ' + DATA.DOCKER_CODES_PATH + '/' + codeName + '.cpp -o ' + DATA.DOCKER_EXES_PATH + '/' + exeName
        elif compileType == 'java':
            compileName = 'javac ' + DATA.DOCKER_CODES_PATH + '/' + codeName + '.java\n'
            compileName += 'mv ' + DATA.DOCKER_CODES_PATH + '/' + exeName + '.class ' + DATA.DOCKER_EXES_PATH
        elif compileType == 'python':
            compileName = 'cp ' + DATA.DOCKER_CODES_PATH + '/' + codeName + '.py ' + DATA.DOCKER_EXES_PATH
        #生成编译的sh文件
        try:
            fileName = 'compile_' + codeName + '_' + exeName + '_' + compileType + '.sh'
            p = Popen('touch ' + DATA.HOST_SHELL_PATH + '/' + fileName,shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
            file = open(DATA.HOST_SHELL_PATH + '/' + fileName,"w")
            file.write('#! /bin/bash\n')
            file.write(compileName + '\n')
            file.write("echo $?")
            Popen("chmod 777 " + DATA.HOST_SHELL_PATH + '/' + fileName,shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
        except Exception,e:
            return False
        return True

    @staticmethod
    def runContainer(exeName, interpreter, param):
        """
        :param exeName: 要运行的可执行文件名
        :param param: 要传入的参数
        :param interpreter: 要运行的解释器名[C++,C,JAVA,PYTHON]
        :return:
        """
        #当shell语句成功实现才返回真，否则返回值，不进以后续操作
        if not OJRunner.createRunShellFile(exeName, interpreter, param):
            return False
        fileName = 'run_' + exeName + '_' + interpreter + '.sh'
        result = DockerRunner.runProgram(fileName)
        return result

    @staticmethod
    def createRunShellFile(exeName, interpreter, param = []):
        """
        :param exeName: 要运行的可执行文件名
        :param param: 要传入的参数
        :param interpreter: 要运行的解释器名[Cpp,C,JAVA,PYTHON]
        :return:
        """
        #将参数用echo的方法输出，并利用|符号做为执行的文件的输入
        exeSentence = 'time ('
        if len(param) > 0:
            exeSentence += 'echo '
            for item in param:
                exeSentence += (str(item) + ' ')
            exeSentence += ' | '
        if interpreter == 'c' or interpreter == 'cpp':
            interpreterValue = ''
        exeSentence += (interpreterValue + ' .' + DATA.DOCKER_EXES_PATH + '/' + exeName + ' )')
        #生成编译的sh文件
        try:
            fileName = 'run_' + exeName + '_' + interpreter + '.sh'
            p = Popen('touch ' + DATA.HOST_SHELL_PATH + '/' + fileName,shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
            file = open(DATA.HOST_SHELL_PATH + '/' + fileName,"w")
            file.write('#! /bin/bash\n')
            file.write(exeSentence + '\n')
            Popen("chmod 777 " + DATA.HOST_SHELL_PATH + '/' + fileName,shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
        except Exception,e:
            return False
        return True

    @staticmethod
    def analysisResult(result, targetResult={}):
        """
        :param result: 要被验证的结果
        :param targetResult: 目标结果
        :return:对比的结果{0:超时，1:答案错，2:正确答案}
        """
        sysTime = None#存放运行的系统时间
        #检测是否是被杀死而终结
        time = re.compile(r'Killed',re.X)
        match = time.findall(result)
        if len(match) != 0:
            return 'Time Limit Exceeded'
        #获取系统时间
        time = re.compile(r'sys\s*\d*m\d*.\d*s',re.X)
        match = time.findall(result)
        time = re.compile(r'\d*m\d*.\d*s',re.X)
        sysTime = time.findall(match[0])
        #获取计算结果
        targetList = targetResult['answer']
        #验证输出结果
        for item in targetList:
            pattern = re.compile("(?<![\S*])" + str(item) + "(?![\S*])", re.M)
            match = pattern.search(result)
            if match == None:
                return 'Wrong Answer'
        #验证输出数量
        pattern = re.compile(r'\n', re.X)
        match = pattern.findall(result)
        if len(match) - 4 != len(targetList):
            return 'Output Limit Exceeded'
        #验证格式是否出错
        pattern = re.compile(r'\n',re.X)
        match = pattern.split(result)
        for i in range(0, len(targetList)):
            matchStr = targetList[i]
            if len(str(matchStr)) != len(match[i]):
                return 'Presentation Error'
        return 'Accepted'

    @staticmethod
    def produce():
        #每10秒钟往数据库中取出待评测项一次
        while True:
            OJRunner.mutex = False
            data = DataBase.DataBaseLinker.getInstance().execute("select * from Submit where result='Waiting'")
            for item in data:
                OJRunner.queue.append(item)
            OJRunner.mutex = True
            time.sleep(10)

    @staticmethod
    def waitingDataBase():
        while True:
            #因数据库不能同时访问，所以只有当数据库信号量为真时，才可进行访问
            if OJRunner.databaseMuxter:
                OJRunner.databaseMuxter = False
                break
            time.sleep(0.1)

    @staticmethod
    def customer(threadId):
        """
        :param threadId: 本线程在进程的是第几个由编写者创建的
        :return:None
        """
        while True:
            if OJRunner.customerMuxter and OJRunner.mutex:
                time.sleep(0.5)
            #进程同步，在若在没人访问队列时，访问并把信号量设为False
            OJRunner.customerMuxter = False
            if len(OJRunner.queue) > 0:
                #取取队列头，并清掉它
                code = OJRunner.queue[0]
                OJRunner.queue.remove(code)
                #允许它人访问，将信号量置为True
                OJRunner.customerMuxter = True
                if code['type']=='cpp':
                    compileType = 'cpp'
                elif code['type'] == 'C':
                    compileType = 'c'
                elif code['type'] == 'JAVA':
                    compileType = 'java'
                else:
                    compileType = 'python'
                #进行编译,若编译失败则返回False，则在数据库中将记录更新为Compilation Error
                if not OJRunner.compile(code['codeName'],code['codeName'],compileType):
                    OJRunner.waitingDataBase()
                    DataBase.DataBaseLinker.getInstance().execute("update Submit set result='compilation error' where codeName='" + code['codeName'] + "'")
                    OJRunner.databaseMuxter = True
                    return
                #从数据库取出测试数据后，进行运行
                #因数据库不能同时访问，所以只有当数据库信号量为真时，才可进行访问,拿到数据库访问权，访问该问题编号对应的洞晓试数据
                OJRunner.waitingDataBase()
                data = list(DataBase.DataBaseLinker.getInstance().execute("select * from TestData where question_id='" + code['question_id'] + "'"))
                OJRunner.databaseMuxter = True
                #执行十次运行，每次随机选出一组测试案例，并将未被测试数据的长度的最后一组代替当前被选种的组，且未测试数据长度减一
                i = 0
                acceptSuccess = True#用来标识是否成功AC
                dictLength = len(data)
                while i < DATA.JUDGEMENT_TIMES:
                    target = {}
                    position = random.randint(0,dictLength-1)
                    #将结果以JSON的格式进行解析
                    testData = json.loads(data[position]['test_data'])
                    targetResult = json.loads(data[position]['result_data'])
                    target['answer'] = targetResult
                    result = OJRunner.runContainer(code['codeName'], compileType, testData)
                    OJResult = OJRunner.analysisResult(result, target)
                    print OJResult
                    #检测结果是否为AC，若不是则写入数据库跳出，执行下一份代码，若是则继续评测
                    if OJResult != 'Accepted':
                        acceptSuccess = False#AC失败，将标识设为False
                        OJRunner.waitingDataBase()
                        DataBase.DataBaseLinker.getInstance().execute("update Submit set result='" + OJResult + "' where codeName='" + code['codeName'] + "'")
                        OJRunner.databaseMuxter = True
                        break
                    #将最后一个赋值给当前随机的这个，并总未测试数据总长减一
                    data[position] = data[dictLength-1]
                    dictLength -= 1
                    i += 1
                if acceptSuccess:
                    DataBase.DataBaseLinker.getInstance().execute("update Submit set result='Accepted' where codeName='" + code['codeName'] + "'")
            else:
                OJRunner.customerMuxter = True
                print 'Thread.' + str(threadId) + ' is sleeping......'
                time.sleep(10)

    @staticmethod
    def timeSupervisor():
        pass




















