#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command

class Seboleitor(Base_Command.Base_Command):

    def translate(self):
        if len(self.args) > 1:
            tt = args.replace('u', 'l')
            tt = tt.replace('ç', 'ss')
            tt = tt.replace('us', 'os')
            tt = tt.replace('ce', 'se')
            self.parent.conn.privmsg(self.channel, tt)
        else:
            return False

    def run(self):
        self.translate()
