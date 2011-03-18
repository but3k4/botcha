#  -*- coding: latin-1 -*-
#
"""
search.py - lokky search module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
from mechanize import Browser, _http
from BeautifulSoup import BeautifulSoup

class Search(object):

    def __init__(self, qtde=3):
        self.qtde = qtde
        self.base_url = { 'google': 'http://www.google.com.br', 'youtube': 'http://www.youtube.com', 'cet': 'http://cetsp1.cetsp.com.br' }

    def get_html(self, u):
        self.header = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'
        self.conn = Browser()
        self.conn.addheaders = [('User-agent', self.header)]
        self.conn.set_handle_robots(False)
        self.conn.set_handle_redirect(True)
        self.conn.set_handle_referer(True)
        self.conn.set_handle_refresh(_http.HTTPRefreshProcessor(), max_time=1)
        self.conn.open(u)
        self.page = self.conn.response().read()
        return BeautifulSoup(self.page)

    def google(self, s):
        search = "/search?source=ig&hl=pt-BR&rlz=&q=%s&btnG=Pesquisa+Google&meta=" % s.replace(' ', '+')
        url = self.base_url['google'] + search
        try:
            soup = self.get_html(url)
            result = soup.findAll('div', attrs={'id': 'res'})[0].findAll('li', attrs={'class': 'g'})
            urls = []
            if len(result) > 0:
                count = 0
                for link in result:
                    if str(link.h3.a['href'])[:4] == 'http':
                        urls.append(link.h3.a['href'])
                        count += 1
                    if count >= self.qtde:
                        break
                return urls
            else:
                urls.append("nenhum resultado encontrado para %s" % s)
                return urls
        except:
                urls.append("erro na consulta, nao consegui fazer o parse para %s" % s)
                return urls

    def youtube(self, s):
        search = "/results?search_query=%s&aq=f" % s.replace(' ', '+')
        url = self.base_url['youtube'] + search
        try:
            soup = self.get_html(url)
            result = soup.findAll('div', attrs={'class': 'result-item *sr '}, limit=self.qtde)
            urls = []
            if len(result) > 0:
                for link in result:
                    urls.append(self.base_url['youtube'] + link.a['href'])
                return urls
            else:
                urls.append("nenhum resultado encontrado para %s" % s)
                return urls
        except:
                urls.append("erro na consulta, nao consegui fazer o parse para %s" % s)
                return urls

    def cet(self):
        search = "/monitransmapa/agora/"
        url = self.base_url['cet'] + search
        soup = self.get_html(url)
        dados = {
            'hora': soup.find('div', id="hora").findAll(text=True)[0],
            'lentidao': soup.find('div', id="lentidao").findAll(text=True)[0],
            'tendencia': str(soup.find('div', id="tendencia").findAll(True)).split()[2].split("=")[1].replace('"', '').replace('ALTA', 'aumentar').replace('BAIXA', 'diminuir').replace('ESTAVEL', 'estavel'),
        }
        lentidao = int(dados['lentidao'])
        if lentidao >= 20 and lentidao <= 49:
            resultado = "transito suave, %(lentidao)s km de congestionamento, tendencia: %(tendencia)s, atualizado as %(hora)s" % dados
        elif lentidao >= 50 and lentidao <= 89:
            resultado = "transito bom, %(lentidao)s km de congestionamento, tendencia: %(tendencia)s, atualizado as %(hora)s" % dados
        elif lentidao >= 90 and lentidao <= 119:
            resultado = "transito ja ta ficando foda, %(lentidao)s km de congestionamento, tendencia: %(tendencia)s, atualizado as %(hora)s" % dados
        elif lentidao >= 120 and lentidao <= 149:
            resultado = "transito fudido, %(lentidao)s km de congestionamento, tendencia: %(tendencia)s, atualizado as %(hora)s" % dados
        elif lentidao >= 150 and lentidao <= 169:
            resultado = "voce se fodeu, %(lentidao)s km de congestionamento, tendencia: %(tendencia)s, atualizado as %(hora)s" % dados
        elif lentidao >= 170 and lentidao <= 189:
            resultado = "voce tomou no cu filho da puta, %(lentidao)s km de congestionamento, tendencia: (%(tendencia)s), atualizado as %(hora)s" % dados
        elif lentidao >= 190 and lentidao <= 209:
            resultado = "o que voce vai fazer com %(lentidao)s km de congestionamento? vai pra onde? vai tomar no cu neh? a tendencia eh (%(tendencia)s), atualizado as %(hora)s" % dados
        elif lentidao >= 210:
            resultado = "caralho mano, fica onde voce ta, aproveita e vai fazer algo util filho da puta, ta com %(lentidao)s km de congestionamento, voce vai pra onde? a tendencia eh (%(tendencia)s), atualizado as %(hora)s" % dados

        return resultado
