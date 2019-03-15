#!/usr/bin/python
# -*- coding:utf-8 -*-

import ADS1256
import config
import threading

class ADS1256_controller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ads1256 = ADS1256.ADS1256()

    def run(self):
        self.ads1256.ADS1256_Init()
        while True:
            pass

'''
try:
    print("ADS1256 test demo")
    ads1256 = ADS1256.ADS1256()
    ads1256.ADS1256_Init()
    # ads1256.ADS1256_GetAll()
    ads1256.ADS1256_GetoneChannel(3)

except :
    # print 'traceback.format_exc():\n%s' % traceback.format_exc()
    exit()
'''

