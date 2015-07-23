# _*_ coding:utf-8 _*_
__author__ = 'xp'

import time
import threading

from PathData import DATA
from Customer import Customer
from Manufacturer import Manufacturer


class OJRunner:
    def __init__(self):
        self.manufactureThread = threading.Thread(target=Manufacturer.getInstance().get_data_from_db)
        self.customerThread = []
        for i in range(0, DATA.THREAD_TOTAL):
            customer = Customer()
            thread = threading.Thread(target=customer.consumption)
            self.customerThread.append(thread)

    def start_judgement(self):
        self.manufactureThread.start()
        for item in self.customerThread:
            item.start()

