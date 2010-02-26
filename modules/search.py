#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
"""
search.py - lokky search module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

class Search(object):

    def __init__(self, qtde=3):
        self.qtde = qtde
        self.conn = Browser()
        self.header = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'
        self.conn.addheaders = [('User-agent', self.header)]
        self.conn.set_handle_robots(False)

    def google(self, s):
        search = s.replace(' ', '+')

        base = 'http://www.google.com.br/search?'
        query = "source=ig&hl=pt-BR&rlz=&q=%s&btnG=Pesquisa+Google&meta=" % search
        
        query_url = base + query
        self.conn.open(query_url)
    
        result_page = self.conn.response().read()
    
        bsoup = BeautifulSoup(result_page)
        result = bsoup.findAll('div', attrs={'id': 'res'})[0]
        list = result.findAll('li', attrs={'class': 'g'})
        
        urls = []
        if len(list) > 0:
            for r in list[0:self.qtde]:
                link = r.h3.a
                urls.append(link['href'])
        
            return urls
        else:
            urls.append("nenhum resultado encontrado para %s" % search.replace('+',' '))
            return urls

    def youtube(self, s):
        search = s.replace(' ', '+')

        base = 'http://www.youtube.com'
        query = "/results?search_query=%s&search_type=&aq=f" % search

        query_url = base + query
        self.conn.open(query_url)

        result_page = self.conn.response().read()

        bsoup = BeautifulSoup(result_page)
        result = bsoup.findAll('div', attrs={'class': 'video-short-title'})[0:self.qtde]

        urls = []
        if len(result) > 0:
            for link in result:
                r = link.a
                urls.append(base + r['href'])

            return urls
        else:
            urls.append("nenhum resultado encontrado para %s" % search.replace('+',' '))
            return urls

    def mininova(self, s):
        search = s.replace(' ', '+')

        base = 'http://www.mininova.org'
        query = '/search/' + search + '/seeds'

        query_url = base + query
        self.conn.open(query_url)

        result_page = self.conn.response().read()

        bsoup = BeautifulSoup(result_page)
        result = bsoup.findAll('a')

        x = 0
        urls = []
        for link in result:
            if link['href'].find('/tor/') != -1:
                urls.append(base + link['href'])
                x += 1
                if x >= self.qtde: break

        if len(urls) > 0:
            return urls
        else:
            urls.append("nenhum resultado encontrado para %s" % search.replace('+',' '))
            return urls
