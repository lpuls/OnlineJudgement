#/usr/bin/env python
__author__ = 'xp'

import time
import docker
from PathData import DATA
from threading import Thread
from OJRunner import OJRunner
from DataBase import DataBaseLinker
#from DockerRunner import DockerRunner

def kill(s):
    timeTotal = 0
    while True:
        timeTotal += 1
        if timeTotal > 10:
            print 'It is time to kill !'
            dockerLinker.stop(container=s['Id'])
            dockerLinker.remove_container(container=s['Id'])
            break
        time.sleep(1)


if __name__ == '__main__':
    dockerLinker = docker.Client(base_url='unix://var/run/docker.sock')
    s = dockerLinker.create_container(image='xpsama/xp_oj_compile:v1.2', command=['/bin/bash'], volumes=[DATA.DOCKER_SHELL_PATH,DATA.DOCKER_EXES_PATH], stdin_open=True, tty=False)
    print s
    p = dockerLinker.start(container=s['Id'],binds={DATA.HOST_SHELL_PATH:{'bind':DATA.DOCKER_SHELL_PATH,'ro': False},
                                                                       DATA.HOST_EXES_PATH:{'bind':DATA.DOCKER_EXES_PATH,'ro':False}})
    k = dockerLinker.exec_create(container=s['Id'], cmd=["./home/shellFiles/run.sh"], stdout=True, stderr=True, tty=True)
    t = dockerLinker.exec_create(container=s['Id'], cmd=["./home/exes/run.sh"], stdout=True, stderr=True, tty=True)
    #k = dockerLinker.execute(container=s['Id'], cmd=['ls'], stdout=True, stderr=True, stream=False, tty=False)
    print k
    q = Thread(target=kill, args=(s,))
    q.start()
    print '0'
    #resultI = dockerLinker.exec_start(k['Id'])
    resultII = dockerLinker.exec_start(t['Id'])
    #print resultI
    print '1'
    print resultII
    #print dockerLinker.logs(container=s['Id'], stdout=True)
    print '2'
    try:
        dockerLinker.stop(container=s['Id'])
        dockerLinker.remove_container(container=s['Id'])
    except Exception,e:
        print e
    finally:
        print 'Over'
    #print DockerRunner.runProgram('CreateFile.sh')
    #result = DataBaseLinker.getInstance().execute("update Submit set result='runtime error' where codeName='xp_0000_201541834233_cpp'")
    #print result