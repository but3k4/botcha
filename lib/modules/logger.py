#  -*- coding: utf-8 -*-
#
"""
logger.py - lokky logger module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
import time
import os
import sys

class Logger(object):

    def __init__(self, logdir='log'):
        self.debug = 0
        self.logdir = logdir

    def __call__(self, string):
        logdir = os.path.join(self.logdir, time.strftime("%Y"), time.strftime("%m"))
        filename = "%s.log" % (os.path.join(logdir, time.strftime("%Y%m%d")))
        string = "[ %s ] %s" % (time.strftime("%d/%m/%Y %H:%M:%S"), string)
        if not os.path.exists(logdir):
            os.makedirs(logdir, 0755)
        file = open(filename, 'a')
        file.write("%s\n" % string)
        if self.debug:
            sys.stdout.write("%s\n" % string)
        file.close()

    def _debug(self, debug=0):
        if debug == 1:
            self.debug = 1
