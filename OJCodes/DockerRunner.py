# _*_ coding:utf-8 _*_
__author__ = 'xp'

import time
import docker
import random

from PathData import DATA


class DockerRunner:

    __dockerRunner = None

    def __init__(self):
        try:
            DockerRunner.__dockerLinker = docker.Client(base_url='unix://var/run/docker.sock')
        except Exception, e:
            error_log = file(DATA.HOST_ERROR_LOG_PATH + '/create_link_docker_' +
                             str(time.time()) + str(random.randint(1000, 9999)) + '.log', 'w')
            error_log.write(e.message)
            error_log.close()

    @staticmethod
    def getInstance():
        if DockerRunner.__dockerRunner is None:
            DockerRunner.__dockerRunner = DockerRunner()
        return DockerRunner.__dockerRunner

    def createContainer(self, type):
        container = None
        binds = {}  # binds is the relationship of host and docker what the path of files
        volumes = []  # volumes is which paths in the docker
        # the type is COMPILE and RUN, but their path is different
        if type.upper() == 'COMPILE':
            binds = {DATA.HOST_SHELL_PATH: {'bind': DATA.DOCKER_SHELL_PATH, 'ro': False},
                     DATA.HOST_CODES_PATH: {'bind': DATA.DOCKER_CODES_PATH, 'ro': False},
                     DATA.HOST_EXES_PATH: {'bind': DATA.DOCKER_EXES_PATH, 'ro': False}}
            volumes = [DATA.DOCKER_SHELL_PATH, DATA.DOCKER_CODES_PATH, DATA.DOCKER_EXES_PATH]
        else:
            binds = {DATA.HOST_SHELL_PATH: {'bind': DATA.DOCKER_SHELL_PATH, 'ro': False},
                     DATA.HOST_EXES_PATH: {'bind': DATA.DOCKER_EXES_PATH, 'ro': False}}
            volumes = [DATA.DOCKER_SHELL_PATH, DATA.DOCKER_CODES_PATH, DATA.DOCKER_EXES_PATH]
        # create a docker container and run it
        try:
            container = DockerRunner.__dockerLinker.create_container(image=DATA.DOCKER_IMAGE_NAME,
                                                                     command=['/bin/bash'], volumes=volumes,
                                                                     stdin_open=True, tty=False)
            DockerRunner.__dockerLinker.start(container=container['Id'], binds=binds)
        except Exception, e:
            error_log = file(DATA.HOST_ERROR_LOG_PATH + '/create_docker_container_' +
                             str(time.time()) + str(random.randint(1000, 9999)) + '.log', 'w')
            error_log.write(e.message)
            error_log.close()
        finally:
            return container

    def exec_command(self, container, cmd=[]):
        try:
            exec_id = DockerRunner.__dockerLinker.exec_create(container=container['Id'], cmd=cmd, stdout=True, stderr=True, tty=False)
            k = DockerRunner.__dockerLinker.exec_start(exec_id['Id'])
        except Exception, e:
            error_log = file(DATA.HOST_ERROR_LOG_PATH + '/exec_docker_cmd_' +
                             str(time.time()) + str(random.randint(1000, 9999)) + '.log', 'w')
            error_log.write(e.message)
            error_log.close()
            return None
        return k

    def remove_container(self, container):
        try:
            DockerRunner.__dockerLinker.stop(container=container['Id'])
            DockerRunner.__dockerLinker.remove_container(container=container['Id'])
        except Exception,e:
            error_log = file(DATA.HOST_ERROR_LOG_PATH + '/remove_docker_container_' +
                            str(time.time()) + str(random.randint(1000, 9999)) + '.log', 'w')
            error_log.write(e.message)
            error_log.close()
            return False
        return True
