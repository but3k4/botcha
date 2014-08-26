#  -*- coding: utf-8 -*-
#
"""
web.py - lokky web module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
import httplib2
from bs4 import BeautifulSoup
import xml.dom.minidom
import urllib
import json

class Web(object):

    def __init__(self):
        pass

    def get(self, url):
        sock = httplib2.Http(timeout=10)
        try:
            headers, response = sock.request(url)
            if headers['status'] in (200, '200'):
                return response
        except:
            return False

    def html(self, data):
        if isinstance(data, str):
            return BeautifulSoup(data)
        else:
            return False

    def encode(self, data):
        return urllib.urlencode(data)

    def xml(self, data):
        if isinstance(data, str):
            return xml.dom.minidom.parseString(data)
        else:
            return False

    def json(self, data):
        if isinstance(data, str):
            return json.loads(data)
        else:
            return False
