#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import web
from types import *

class Transito(Base_Command.Base_Command):

    def transito(self):
        web = Web()
        answer = web.html('http://cetsp1.cetsp.com.br/monitransmapa/agora/')
        if type(answer) is not NoneType:
            dados = {
                'hora': answer.find('div', id="hora").findAll(text=True)[0],
                'lentidao': answer.find('div', id="lentidao").findAll(text=True)[0],
            }
            result = "%(lentidao)s km de transito, atualizado as %(hora)s" % dados
            self.parent.conn.privmsg(self.channel, result)
        else:
            return False

    def run(self):
        self.transito()
