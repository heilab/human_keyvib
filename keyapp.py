from __future__ import print_function
import socket
import time
import argparse
from contextlib import closing
import sys
import numpy as np
import time
import _pickle as pickle
import matplotlib.pyplot as plt
import serial

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import threading
import csv
from pyhooked import Hook, KeyboardEvent, MouseEvent


class KeyWatcher(threading.Thread):

    def __init__(self, record=False, rec_time=10):
        super(KeyWatcher, self).__init__()
        self.setDaemon(True)
        self.keys = []
        self.record = record
        self.rec_time = rec_time
        os.chdir("C:\\Users\\heilab\\Desktop\\Arduino_practice\\keyvib")
        if self.record:
            print("key recording start...")
            self.folder_path = record
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
        self.recording_time = time.time() * 1000

    def get_keys(self):
        return self.keys

    def reset(self):
        self.keys = []

    def check_record(self):
        if self.record:
            now = time.time() * 1000
            if now - self.recording_time > self.rec_time * 1000:
                with open(self.folder_path + '/output_' + str(int(self.recording_time)) + '.csv', 'w') as f:
                    writer = csv.writer(f, lineterminator='\n') 
                    writer.writerows(self.keys)
                self.keys = []
                self.recording_time = now
        else:
            print(self.keys)

    def run(self):
        def handle_events(args):
            if isinstance(args, KeyboardEvent):
                if args.event_type == "key up" or args.event_type == "key down":
                    e = 1 if args.event_type == "key down" else 0
                    self.check_record()
                    self.keys.append([time.time() * 1000, args.key_code, e]) # [unix time, keyコード, キーが押されたか(1)離されたか(0)]
                if args.current_key == 'Q' and args.event_type == 'key down' and 'Lcontrol' in args.pressed_key:
                    hk.stop()
                    print('Quitting.')

            if isinstance(args, MouseEvent):
                if args.mouse_x == 300 and args.mouse_y == 400:
                    print("Mouse is at (300,400") 

        hk = Hook()  # make a new instance of PyHooked
        hk.handler = handle_events  # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
        hk.hook()  # hook into the events, and listen to the press

def arduino(sec):
    print("arduino is working")
    ser1 = serial.Serial("COM1")  # COMポート(Arduino接続)
    xg = [0]*100              # 温度格納
    yg = [0]*100            # 温度格納
    zg = [0]*100
    t = np.arange(0,100,1)
    
    while True:
        start_time = time.time()
        f1 = open(str(start_time) + "_keyvib.csv","w")
        while True:
            deg_str_ls1 = ser1.readline().decode().rstrip("\r\n")
            deg_str_j1 = str(time.time()) + "," + str(deg_str_ls1) + "\n"
            f1.write(deg_str_j1)

            if time.time() - start_time > sec:
                f1.close()
                break

def watch(record, sec):
    print("watch is working")
    watcher = KeyWatcher(record, rec_time=sec)
    watcher.start()
#    arduino(sec)
    while True:
        try:
            while True:
                a = 1
        except KeyboardInterrupt:
            while True:
                print("END...")
                sys.exit()

if __name__ == '__main__':
    sec = 10
    record = './record/info'
    print("get typing info and sound")
    thread_1 = threading.Thread(target=watch(record,sec))
    thread_2 = threading.Thread(target=arduino(sec))

    thread_1.start()
    thread_2.start()



'''
while True:
    while True:
        if(time.time()/60 == 0)

start = time.time()
num=0
while True:
    if time.time()-start > num*60:
        save(flag)
        num+=1
    watch()
'''