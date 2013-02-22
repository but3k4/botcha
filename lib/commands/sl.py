#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.twitterz import Twitterz

class Sl(Base_Command.Base_Command):

    def sl(self):
        tw = Twitterz()
        try:
            self.parent.conn.privmsg(self.channel, tw.ilikegirlz())
        except:
            return False

    def run(self):
        self.sl()
