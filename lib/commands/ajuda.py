#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command

class Ajuda(Base_Command.Base_Command):

    def ajuda(self):
        self.parent.conn.privmsg(self.channel, '%s' % ('-- comandos disponiveis --'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!ajuda'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!quote (!add quote)'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!xinga (!add xingamento)'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!lero'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!btc'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!transito'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!sl'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!dollar'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!ipinfo'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!sebolaitor'))


    def run(self):
        self.ajuda()
