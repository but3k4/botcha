#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import Web
from types import *
from lxml import html

class Ipinfo(Base_Command.Base_Command):

    def ipinfo(self):
        web = Web()
        uri = 'http://whatismyipaddress.com/ip/'
        answer = web.html(web.get(uri + self.args[0]))

        if type(answer) is not NoneType:
            th = answer.findAll('th')
            td = answer.findAll('td')

            infos = []
            for x in range(len(td)):
                key = th[x].string.lower().strip()
                value = str(html.fromstring(str(td[x]).replace('\n', '')).text).strip()
                if not value.startswith('None'):
                    infos.append("%s %s" % (key, value))
        else:
            return False

        if len(infos):
            self.parent.conn.privmsg(self.channel, ', '.join(infos))

    def run(self):
        self.ipinfo()
