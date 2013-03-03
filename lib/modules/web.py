#  -*- coding: utf-8 -*-
#
"""
web.py - lokky web module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
import httplib2
import BeautifulSoup
import xml.dom.minidom
import json

class Web(object):

    def __init__(self):
        pass

    def get(self, url):
        sock = httplib2.Http(timeout=5)
        headers, response = sock.request(url)
        if headers['status'] in (200, '200'):
            return response

    def html(self, data):
        return BeautifulSoup.BeautifulSoup(data)

    def xml(self, data):
        return xml.dom.minidom.parseString(data)

    def json(self, data):
        return json.loads(data)
