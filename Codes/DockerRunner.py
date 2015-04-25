#coding:utf-8
__author__ = 'xp'

import docker
from PathData import DATA

class DockerRunner:
    """
    @:var __dockerLinker: 用来连接docker的变量
    """
    __dockerLinker = None

    @staticmethod
    def linkDocker():
        """
        @:return:是否成功连上docker
        """
        try:
            DockerRunner.__dockerLinker = docker.Client(base_url='unix://var/run/docker.sock')
        except Exception,e:
            return False
        return True

    @staticmethod
    def runCompile(shell):
        """
        @:param shell: 要让docker执行的sh文件所在
        @:return:执行shell后得到的结果
        """
        r = None
        if DockerRunner.__dockerLinker == None:
            DockerRunner.linkDocker()
        #create a container and run it
        try:
            s = DockerRunner.__dockerLinker.create_container(image='xp_oj_compile:v2', volumes=[DATA.DOCKER_SHELL_PATH,DATA.DOCKER_CODES_PATH, DATA.DOCKER_EXES_PATH], stdin_open=True, tty=False)
            DockerRunner.__dockerLinker.start(container=s['Id'],binds={DATA.HOST_SHELL_PATH:{'bind':DATA.DOCKER_SHELL_PATH,'ro': False},
                                                                       DATA.HOST_CODES_PATH:{'bind':DATA.DOCKER_CODES_PATH,'ro':False},
                                                                       DATA.HOST_EXES_PATH:{'bind':DATA.DOCKER_EXES_PATH,'ro':False}})
            r = DockerRunner.__dockerLinker.execute(container=s['Id'], cmd=['.'+ DATA.DOCKER_SHELL_PATH + '/' + shell], stdout=True, stderr=True, stream=False, tty=False)
            DockerRunner.__dockerLinker.stop(container=s['Id'])
            DockerRunner.__dockerLinker.remove_container(container=s['Id'])
        except Exception,e:
            #理论上这个错误应该写进日志文件
            print e
            pass
        finally:
            return r

    @staticmethod
    def runProgram(shell):
        """
        很相吐槽，我居然因为数据卷只差了一个而写了两个方法==真TM有病
        @:param shell: 要让docker执行的sh文件所在
        @:return:执行shell后得到的结果
        """
        k = None
        if DockerRunner.__dockerLinker == None:
            DockerRunner.linkDocker()
        #create a container and run it
        try:
            s = DockerRunner.__dockerLinker.create_container(image='xp_oj_compile:v2', volumes=[DATA.DOCKER_SHELL_PATH,DATA.DOCKER_EXES_PATH], stdin_open=True, tty=False)
            DockerRunner.__dockerLinker.start(container=s['Id'],binds={DATA.HOST_SHELL_PATH:{'bind':DATA.DOCKER_SHELL_PATH,'ro': False},
                                                                       DATA.HOST_EXES_PATH:{'bind':DATA.DOCKER_EXES_PATH,'ro':False}})
            k = DockerRunner.__dockerLinker.execute(container=s['Id'], cmd=['.'+ DATA.DOCKER_SHELL_PATH + '/' + shell], stdout=True, stderr=True, stream=False, tty=False)
            DockerRunner.__dockerLinker.logs(container=s['Id'])
            DockerRunner.__dockerLinker.stop(container=s['Id'])
            DockerRunner.__dockerLinker.remove_container(container=s['Id'])
        except Exception,e:
            #理论上这个错误应该写进日志文件
            pass
        finally:
            return k
