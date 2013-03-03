#  -*- coding: utf-8 -*-
#
"""
edbot.py - edbot module based on wyrdbot
from https://github.com/guru-sp/wyrdbot
Copyright 2013, Claudio Borges
Licensed under BSD License.
"""
import urllib
import re

class Edbot(object):

    def __init__(self):
        pass

    def answer(self, message):
        self.message = ' '.join(message.split()[1:])

        params = {
            'server': '0.0.0.0:8085',
            'charset_post': "utf-8",
            'charset': 'utf-8',
            'pure': 1,
            'js': 0,
            'tst': 1,
            'msg': self.message
        }

        options = urllib.urlencode(params)

        url = 'http://www.ed.conpet.gov.br/mod_perl/bot_gateway.cgi'

        try:
            result = urllib.urlopen(url, options)
            return re.sub('<[^<>]*>', '', result.read()).strip('\n')
        except:
            return False
