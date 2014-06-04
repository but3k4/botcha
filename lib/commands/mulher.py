#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.database import Database

class Mulher(Base_Command.Base_Command):

    def mulher(self):
        db = Database()
        self.mulher = None
        try:
            self.mulher = db.select('mulher', 'mulheres', 1)[0][0]
        except:
            return False
        if self.mulher:
            self.parent.conn.privmsg(self.channel, self.mulher)

    def run(self):
        self.mulher()
