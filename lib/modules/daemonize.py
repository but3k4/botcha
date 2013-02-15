#  -*- coding: utf-8 -*-
#
"""
daemonize.py - lokky daemon module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
import os
import sys

class Daemonize(object):

    def __init__(self, logfile="/dev/null"):
        self.logfile = logfile

    def start(self):
        stdin = '/dev/null'
        stdout = self.logfile
        stderr = stdout

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("Error: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        os.chdir(os.getcwd() + '/')
        os.umask(0)
        os.setsid()

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("Error: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        if self.logfile != '/dev/null' and os.path.exists(self.logfile):
            os.unlink(self.logfile)

        si = open(stdin, 'r')
        so = open(stdout, 'a+')
        se = open(stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
