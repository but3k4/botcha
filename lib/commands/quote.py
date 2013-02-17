#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.database import Database

class Quote(Base_Command.Base_Command):

    def quote(self):
        db = Database()
        self.quote = None
        try:
            self.quote = db.select('quote', 'quotes', 1)[0][0]
        except:
            return False
        if self.quote:
            self.parent.conn.privmsg(self.channel, self.quote)

    def run(self, e):
        self.quote()
