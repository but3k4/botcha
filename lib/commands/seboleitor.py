#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.database import Database

class Seboleitor(Base_Command.Base_Command):

    def translate(self):
        letters = { 'u': 'l', 'ç': 'ss', 'us': 'os', 'ce': 'se' }
        args = ' '.join(self.args)
        if len(args) > 1:
            for k, v in letters.iteritems():
                args = args.replace(k, v)
            self.parent.conn.privmsg(self.channel, args)
        else:
            db = Database()
            quote = None
            try:
                quote = db.select('quote', 'quotes', 1)[0][0]
            except:
                return False
            if quote:
                for k, v in letters.iteritems():
                    quote = quote.replace(k, v)
                self.parent.conn.privmsg(self.channel, 'se fosse o sebola, ele diria: %s' % quote)

    def run(self):
        self.translate()
