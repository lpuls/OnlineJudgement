# _*_ coding:utf-8 _*_
__author__ = 'xp'

import time
import random
import threading

from Log import Log
from PathData import DATA
from OJDataBaseAdministrator import OJDataBaseAdministrator as OJDBA


class Manufacturer:

    __manufacturer = None

    def __init__(self):
        self.__queue = []
        self.__mutex = True  # a sign whether can access the __queue
        # self.__thread = None  # this thread is used to get submit from data base

    @staticmethod
    def getInstance():
        if Manufacturer.__manufacturer == None:
            Manufacturer.__manufacturer = Manufacturer()
            # Manufacturer.__manufacturer.__thread = threading.Thread(target=Manufacturer.__manufacturer.getDataFromDB)
            # Manufacturer.__manufacturer.__thread.start()
        return Manufacturer.__manufacturer

    # wait the sign which be call __mutex prevent other thread access the __queue
    def waitMutex(self):
        while True:
            if self.__mutex:
                self.__mutex = False
                break
            time.sleep(0.1)

    # release the sign which be call __mutex to guarantee other thread can access the __queue
    def releaseMutex(self):
        self.__mutex = True

    # get submit which the result is 'waiting' from DB
    def getDataFromDB(self):
        while True:
            Log.ProducerLOG('The length of queue is : ' + str(len(self.__queue)))
            self.waitMutex()
            submits = OJDBA.getSubmitWhichWaiting()
            for item in submits:
                OJDBA.updateRunning(item.getCodeName())
            self.__queue += submits
            self.releaseMutex()
            time.sleep(DATA.MANUFACTURE_SLEEP_TIME)

    # remove the first submit of __queue
    def __removeFromQueue(self, submit):
        try:
            self.waitMutex()
            self.__queue.remove(submit)
            self.releaseMutex()
        except Exception,e:
            errorLog = file(DATA.HOST_ERROR_LOG_PATH + '/remove_queue_' + str(time.time()) + str(random.randint(1000, 9999)) + '.log', 'w')
            errorLog.write(e.message)
            errorLog.close()
            return False
        return True

    # get the first submit  of __queue
    def getQueueHead(self):
        submit = None
        Log.ProducerLOG('Wait the manufacturer mutex')
        self.waitMutex()
        Log.ProducerLOG('Get Head')
        if len(self.__queue) > 0:
            submit = self.__queue[0]
        self.releaseMutex()
        Log.ProducerLOG('Remove Head')
        if submit is not None:
            self.__removeFromQueue(submit)
        return submit