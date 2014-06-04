#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import Web
import re

class Btc(Base_Command.Base_Command):

    def btc(self):
        web = Web()
        try:
            answer = web.html(web.get('http://bitcoinexchangerate.org/c/USD/1'))
            pattern = re.compile('([0-9.]+)')
            result = re.findall(pattern, str(answer.title.string))[0]
            self.parent.conn.privmsg(self.channel, "%s USD / BTC" % round(float(result), 2))
        except:
            return False

    def run(self):
        self.btc()
