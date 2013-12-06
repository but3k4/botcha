#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.database import Database

class Mulher(Base_Command.Base_Command):

    def mulher(self):
        if len(self.args) < 1:
            self.parent.conn.privmsg(self.channel,'%s, deixa de ser burro e mulher alguém. ' % self.nick)
        else:
            db = Database()
            self.mulher = None
            try:
                self.mulher = db.select('mulher', 'mulheres', 1)[0][0]
            except:
                return False
            if self.mulher:
                self.parent.conn.privmsg(self.channel, '%s, %s' % (self.args[0], self.mulher))

    def run(self):
        self.mulher()
