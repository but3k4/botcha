#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import Web

class Chuck(Base_Command.Base_Command):

    def chuck(self):
        web = Web()
        try:
            answer = web.json(web.get("http://api.icndb.com/jokes/random"))
            self.parent.conn.privmsg(self.channel, answer['value']['joke'])
        except:
            return False

    def run(self):
        self.chuck()
