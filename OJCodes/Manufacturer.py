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
        if Manufacturer.__manufacturer is None:
            Manufacturer.__manufacturer = Manufacturer()
            # Manufacturer.__manufacturer.__thread = threading.Thread(target=Manufacturer.__manufacturer.getDataFromDB)
            # Manufacturer.__manufacturer.__thread.start()
        return Manufacturer.__manufacturer

    # wait the sign which be call __mutex prevent other thread access the __queue
    def wait_mutex(self):
        while True:
            if self.__mutex:
                self.__mutex = False
                break
            time.sleep(0.1)

    # release the sign which be call __mutex to guarantee other thread can access the __queue
    def release_mutex(self):
        self.__mutex = True

    # get submit which the result is 'waiting' from DB
    def get_data_from_db(self):
        while True:
            Log.producer_log('The length of queue is : ' + str(len(self.__queue)))
            self.wait_mutex()
            submits = OJDBA.get_submit_which_waiting()
            for item in submits:
                OJDBA.update_running(item.get_code_name())
            self.__queue += submits
            self.release_mutex()
            time.sleep(DATA.MANUFACTURE_SLEEP_TIME)

    # remove the first submit of __queue
    def __remove_from_queue(self, submit):
        try:
            self.wait_mutex()
            self.__queue.remove(submit)
            self.release_mutex()
        except Exception,e:
            error_log = file(DATA.HOST_ERROR_LOG_PATH + '/remove_queue_' + str(time.time()) + str(random.randint(1000, 9999)) + '.log', 'w')
            error_log.write(e.message)
            error_log.close()
            return False
        return True

    # get the first submit  of __queue
    def get_queue_head(self):
        submit = None
        Log.producer_log('Wait the manufacturer mutex')
        self.wait_mutex()
        Log.producer_log('Get Head')
        if len(self.__queue) > 0:
            submit = self.__queue[0]
        self.release_mutex()
        Log.producer_log('Remove Head')
        if submit is not None:
            self.__remove_from_queue(submit)
        return submit
