#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.database import Database

class Help(Base_Command.Base_Command):

    def help(self):
        self.help = None
        self.parent.conn.privmsg(self.channel, '%s' % ('-- comandos disponiveis --'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!help'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!quote (!add quote)'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!xinga (!add xingamento)'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!lero'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!btc'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!transito'))
        self.parent.conn.privmsg(self.channel, '%s' % ('!sl'))

    def run(self):
        self.help()
