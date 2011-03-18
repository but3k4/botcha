#  -*- coding: latin-1 -*-
#
"""
logger.py - lokky logger module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
from time import strftime
from os.path import exists, join
from os import makedirs
from sys import stdout

class Logger(object):

    def __init__(self):
        self.debug = 0

    def __call__(self, string):
        logdir = join('log', strftime("%Y"), strftime("%m"))
        filename = "%s.log" % (join(logdir, strftime("%Y%m%d")))
        string = "[ %s ] %s" % (strftime("%d/%m/%Y %H:%M:%S"), string)
        if not exists(logdir):
            makedirs(logdir, 0755)
        file = open(filename, 'a')
        file.write("%s\n" % string)
        if self.debug:
            stdout.write("%s\n" % string)
        file.close()

    def set_debug(self, debug=0):
        if debug == 1:
            self.debug = 1
