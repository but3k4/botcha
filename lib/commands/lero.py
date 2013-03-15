#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.database import Database

class Lero(Base_Command.Base_Command):

    def lero(self):
        db = Database()
        self.xinga = None
        try:
            self.xinga = db.select('xinga', 'xingamentos', 1)[0][0]
        except:
            return False
        if self.xinga:
            self.parent.conn.privmsg(self.channel, '%s, %s' % ('lero', self.xinga))

    def run(self):
        self.lero()
