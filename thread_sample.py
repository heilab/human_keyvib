#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import threading
import time


class ThreadA(threading.Thread):

    def __init__(self, record=False, rec_time=10):
        super(ThreadA, self).__init__()
        self.setDaemon(True)
        self.count = 0

    def run(self):
        while True:
            self.count += 1
            time.sleep(1)
            print("threadA " + str(self.count))


class ThreadB(threading.Thread):

    def __init__(self, record=False, rec_time=10):
        super(ThreadB, self).__init__()
        self.setDaemon(True)
        self.count = 0

    def run(self):
        while True:
            self.count += 1
            time.sleep(2)
            print("threadB " + str(self.count))


if __name__ == '__main__':
    print("start events")
    a = ThreadA()
    a.setDaemon(True)
    a.start()
    b = ThreadB()
    b.setDaemon(True)
    b.start()
    
    while True:
        c = 1