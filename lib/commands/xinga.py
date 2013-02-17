#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.database import Database

class Xinga(Base_Command.Base_Command):

    def xinga(self):
        db = Database()
        self.xinga = None
        try:
            self.xinga = db.select('xinga', 'xingamentos', 1)[0][0]
        except:
            return False
        if self.xinga:
            self.parent.conn.privmsg(self.channel, self.xinga)

    def run(self):
        self.xinga()
