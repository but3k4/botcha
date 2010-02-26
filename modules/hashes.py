#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
"""
hashes.py - lokky cryptography module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
import md5
from crypt import crypt
from random import choice
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits

class Hashes(object):

    def __init__(self):
        pass

    def genCrypt(self, string):
        string = string.strip()
        LIST = './' + digits + ascii_letters
        salt = '$1$'
        for x in range(0,8):
            salt += choice(LIST)
        salt += '$'
        return crypt(string, salt)

    def genMd5(self, string):
        string = string.strip()
        return md5.new(string).hexdigest()
