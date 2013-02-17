#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.database import Database
from irclib import nm_to_n

class Add(Base_Command.Base_Command):

    def quote(self, string):
        db = Database()
        try:
            db.insert('quotes', string.strip())
        except:
            return False
        return True

    def xingamento(self, string):
        db = Database()
        try:
            db.insert('xingamentos', string.strip())
        except:
            return False
        return True

    def add(self, e):
	nick = nm_to_n(e.source())
        if len(self.args) > 1:
            content = ' '.join(self.args[1:])
            result = None
            if self.args[0] == 'quote':
                result = self.quote(content)
                if result:
                    self.parent.conn.privmsg(self.channel, "%s, %s adicionado." % (nick, self.args[0]))

            if self.args[0] == 'xingamento':
                result = self.xingamento(content)
                if result:
                    self.parent.conn.privmsg(self.channel, "%s, %s adicionado." % (nick, self.args[0]))
	else:
		self.parent.conn.privmsg(self.channel, "%s, deixa de ser burro." % nick)

    def run(self, e):
        self.add(e)
