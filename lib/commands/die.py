#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
import time

class Die(Base_Command.Base_Command):

    def die(self):
        if self.check_admin():
            self.parent.conn.privmsg(self.channel, 'see ya')
            self.parent.die()

    def run(self, e):
        self.die()
