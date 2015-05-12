#/usr/bin/env python
__author__ = 'xp'

#import docker
from PathData import DATA
from DataBase import DataBaseLinker
from DockerRunner import DockerRunner

if __name__ == '__main__':
    print DockerRunner.runProgram('CreateFile.sh')
    """
    dockerLinker = docker.Client(base_url='unix://var/run/docker.sock')
    s = dockerLinker.create_container(image='xpsama/xp_oj_compile:v1.0', command=['/bin/bash'], volumes=[DATA.DOCKER_SHELL_PATH,DATA.DOCKER_EXES_PATH], stdin_open=True, tty=False)
    print s
    p = dockerLinker.start(container=s['Id'],binds={DATA.HOST_SHELL_PATH:{'bind':DATA.DOCKER_SHELL_PATH,'ro': False},
                                                                       DATA.HOST_EXES_PATH:{'bind':DATA.DOCKER_EXES_PATH,'ro':False}})
    k = dockerLinker.exec_create(container=s['Id'], cmd=["./home/shellFiles/CreateFile.sh"], stdout=True, stderr=True, tty=True)
    #k = dockerLinker.execute(container=s['Id'], cmd=['ls'], stdout=True, stderr=True, stream=False, tty=False)
    print k
    print dockerLinker.exec_start(k['Id'])
    #print dockerLinker.logs(container=s['Id'], stdout=True)
    dockerLinker.stop(container=s['Id'])
    dockerLinker.remove_container(container=s['Id'])

    #print DockerRunner.runProgram('CreateFile.sh')
    #result = DataBaseLinker.getInstance().execute("update Submit set result='runtime error' where codeName='xp_0000_201541834233_cpp'")
    #print result
    """