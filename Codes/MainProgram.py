#coding:utf-8
#!/usr/bin/env python
__author__ = 'xp'

import docker
import threading
import DataBase
from subprocess import *

DOCKER_DATA_VOLUMES_NAME = "/home/codes"
DOCKER_DATA_VOLUMES_PATH = "/home/xp/codes"
SHELL_FILE_PATH = "/home/xp/Codes"

class OJRunner:
    """
    @:var queue: 存放待测代码的队列
    @:var mutex: 进程同步的标识
    @:var customerMuxter: 消费者之间，在读取OJRunner.queue时的信号量
    @:var threadTime : 记录每个线程开启运行容器的时间
    @:var threads : 存放每个线程的列表
    """
    queue = []
    mutex = False
    customerMuxter = False
    threadTime = []
    threads = []

    @staticmethod
    def running():
        pass

    @staticmethod
    def compile(codeName, executableName, compilerName):
        """
        :param codeName:  要被执行的代码文件名
        :param executableName: 要生成的执行文件名
        :param compilerName: 先用的编译器名
        :return: 是否编译成功(True or False)
        """
        pass
        """
        p = Popen("sh compile",shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
        result = p.communicate(codeName + '\n' + executableName + '\n' + compilerName)
        #result = p.communicate('test.cpp\ncode2\n.cpp')
        if result[0] != 'success\n':
            return False
        return True
        """

    @staticmethod
    def create(fileName, executeableName, stdinData=[]):
        """
        :param fileName: 要生成的文件名
        :param executeableName: 要被执行的文件
        :param stdinData: 要输入的数据
        :return: 无
        """
        pass
        """
        global DOCKER_DATA_VOLUMES_NAME
        global DOCKER_DATA_VOLUMES_PATH
        global SHELL_FILE_PATH
        #create a shell file and write command to it
        p = Popen("touch "+DOCKER_DATA_VOLUMES_PATH + '/' + fileName,shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
        file = open(DOCKER_DATA_VOLUMES_PATH + '/' + fileName,"w")
        file.write('#! /bin/bash\n')
        file.write('cd ' + DOCKER_DATA_VOLUMES_NAME + '\n')
        shellCommand = "time echo "
        for item in stdinData:
            shellCommand += item + " "
        shellCommand += " | ./" + executeableName
        file.write(shellCommand + "\n")
        file.close()
        p = Popen("./chmod.sh",shell=True, stdin=PIPE,stdout=PIPE, close_fds=True)
        result = p.communicate(DOCKER_DATA_VOLUMES_PATH + '/' + fileName)
        """


class DockerRunner:
    """
    @:var c: 用来连接docker的变量
    """

    c = None

    @staticmethod
    def linkDocker():
        """
        用来连接docker
        :return: 无
        """
        DockerRunner.c = docker.Client(base_url='unix://var/run/docker.sock')

    @staticmethod
    def executeProgram(shellPath):
        """
        运行容器
        :param shellPath: 运行容器后要执行的sh文件
        :return: 无
        """
        if DockerRunner.c == None:
            return None
        #create a container and run it
        s = DockerRunner.c.create_container(image='ubuntu', volumes=['/home/codes'], stdin_open=True, tty=False)
        r = DockerRunner.c.start(container=s['Id'],binds={'/home/xp/codes':{'bind':'/home/codes','ro': False}})
        k = DockerRunner.c.execute(container=s['Id'], cmd=['./home/codes/'+shellPath], stdout=True, stderr=True, stream=False, tty=False)
        try:
            DockerRunner.c.stop(container=s['Id'])
            DockerRunner.c.remove_container(container=s['Id'])
        except errno:
            file = open('/mylogs',"w")
            file.seekable()
            file.write(errno)
        finally:
            return k



if __name__ == "__main__":
    #OJRunner.running()
    #for item in OJRunner.queue:
    #    print item
    DockerRunner.linkDocker()
    print type(DockerRunner.c)
    """
    #compile('HelloWorld.java','', 'java')
    #DockerRunner.linkDocker()
    #create("myShell2.sh", "sum", ['100','-1'])
    #result = DockerRunner.executeProgram("myShell2.sh")
    #print result
    """
