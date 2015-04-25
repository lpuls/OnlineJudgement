#coding:utf-8
#!/usr/bin/env python
__author__ = 'xp'

import time
from threading import Thread
from subprocess import *

def moveCodeFile():
    while True:
        p = Popen('/home/xp/TempCodes/MvCodes.sh', stdin=PIPE, stdout=PIPE, stderr=PIPE)
        print p.stderr.read()
        time.sleep(0.01)

if __name__ == "__main__":
    t = Thread(target=moveCodeFile)
    t.start()

