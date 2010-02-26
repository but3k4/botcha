#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
"""
logger.py - lokky logger module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
import time
import os
from sys import stdout

class Logger(object):
    def __init__(self):
        self.debug = 0

    def __call__(self, string):
        base = "log"
        logdir = os.path.join(base, time.strftime("%Y%m"))
        filename = os.path.join(logdir, time.strftime("%Y%m%d") + '.log')
        string = '[' + time.strftime("%d/%m/%Y %H:%M:%S") + ']' + ' ' + string + '\n'
        if os.path.exists(base) == False:
            os.mkdir(base, 0755)
        if os.path.exists(logdir) == False:
            os.mkdir(logdir, 0755)
        file = open(filename, 'a')
        file.write(string)
        if self.debug:
            stdout.write(string)
        file.close()

    def set_debug(self, debug=0):
        if debug == 1:
            self.debug = 1
