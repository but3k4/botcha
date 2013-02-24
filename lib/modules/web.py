#  -*- coding: utf-8 -*-
#
"""
web.py - lokky web module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
import httplib2
import BeautifulSoup

class Web(object):

    def __init__(self):
        pass

    def html(self, url):
        sock = httplib2.Http(timeout=5)
        headers, response = sock.request(url)
        if headers['status'] in (200, '200'):
            return BeautifulSoup.BeautifulSoup(response)
    
    def cet(self):
        try:
            answer_data = self.html('http://cetsp1.cetsp.com.br/monitransmapa/agora/')
        except:
            return False
        dados = {
            'hora': answer_data.find('div', id="hora").findAll(text=True)[0],
            'lentidao': answer_data.find('div', id="lentidao").findAll(text=True)[0],
        }
        return "%(lentidao)s km de transito, atualizado as %(hora)s" % dados
