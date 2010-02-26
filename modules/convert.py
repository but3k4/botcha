#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
"""
binary.py - lokky binary conversion module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""

import re

class Convert(object):

    def __init__(self):
        pass

    def hex2string(self, h):
        result = []
        for i in range(len(h)/2):
            count = i*2
            result.append(chr(int(h[count:count+2],16)))
        return "".join(result)

    def string2hex(self, s):
        result = []
        for c in s:
            result.append("%X" % ord(c))
        return "".join(result)
        
    def string2binary(self, s):
        b = ('0000','0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011','1100','1101','1110','1111')
        result = []
        for l in s:
            x,y = divmod(ord(l), 16)
            result.append(b[x] + b[y])
        return "".join(result)
        
    def binary2string(self, b):
        if len(b) % 8 != 0:
            return "utilize binarios de 8 digitos"
        elif re.compile('[^0-1]').search(b):
            return "%s nao eh binario" % b
        
        count = 0
        result = []
        for r in range(len(b)/8):
            s = 0
            t = 0
            for n in b[count:count+8][::-1]:
                t += int(n) * pow(2, s)
                s += 1
            result.append(t)
            count += 8
        return "".join([chr(c) for c in result])
