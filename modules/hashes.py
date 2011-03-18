#  -*- coding: latin-1 -*-
#
"""
hashes.py - lokky cryptography module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
from md5 import new
from crypt import crypt
from random import choice
from string import ascii_letters, digits

class Hashes(object):

    def __init__(self):
        pass

    def genCrypt(self, string):
        list = './' + digits + ascii_letters
        salt = '$1$'
        for x in range(0,8):
            salt += choice(list)
        salt += '$'
        return crypt(string.strip(), salt)

    def genMd5(self, string):
        return new(string.strip()).hexdigest()
