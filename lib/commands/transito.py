#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.search import Search

class Transito(Base_Command.Base_Command):

    def transito(self):
        search = Search()
        try:
            self.parent.conn.privmsg(self.channel, search.cet())
        except:
            return False

    def run(self, e):
        self.transito()
