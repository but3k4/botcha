#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import web

class Transito(Base_Command.Base_Command):

    def transito(self):
        search = Web()
        try:
            self.parent.conn.privmsg(self.channel, web.cet())
        except:
            return False

    def run(self):
        self.transito()
