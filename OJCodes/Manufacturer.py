# _*_ coding:utf-8 _*_
__author__ = 'xp'

import time

from PathData import DATA
from OJDataBaseAdministrator import OJDataBaseAdministrator as OJDBA


class Manufacturer:

    __manufacturer = None

    def __init__(self):
        self.__queue = []
        self.__mutex = True  # a sign whether can visit the __queue

    @staticmethod
    def getInstance():
        if Manufacturer.__manufacturer == None:
            Manufacturer.__manufacturer = Manufacturer()
        return Manufacturer.__manufacturer

    # wait the sign which be call __mutex to prevent other thread visit the __queue
    def waitMutex(self):
        while True:
            if Manufacturer.getInstance().__mutex:
                Manufacturer.getInstance().__mutex = False
                break
            time.sleep(0.1)

    # release the sign which be call __mutex to guarantee other thread can visit the __queue
    def releaseMutex(self):
        self.__mutex = True

    # get submit which the result is 'waiting' from DB
    def getDataFromDB(self):
        while True:
            self.waitMutex()
            submits = OJDBA.getSubmitWhichWaiting()
            self.__queue += submits
            self.releaseMutex()
            time.sleep(DATA.MANUFACTURE_SLEEP_TIME)

    # get the first submit  of __queue
    def getQueueHead(self):
        self.waitMutex()
        submit = self.__queue[0]
        self.releaseMutex()
        return submit