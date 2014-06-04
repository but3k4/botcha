#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import Web
import re

class Ipinfo(Base_Command.Base_Command):

    def ipinfo(self):
        web = Web()
        uri = 'http://whatismyipaddress.com/ip/'
        try:
            answer = web.html(web.get(uri + self.args[0]))

            if answer:
                th = answer.findAll('th')
                td = answer.findAll('td')

                infos = []
                for x in range(len(td)):
                    key = th[x].string.lower().strip()
                    value = re.sub('\([^()]+\)', '', re.sub('<[^<>]*>', '', str(td[x])).strip('\n').replace('&nbsp;', '').strip())
                    if not value.startswith('None') and len(value):
                        infos.append("%s %s" % (key, value))
            else:
                return False
        except:
            return False

        if len(infos):
            self.parent.conn.privmsg(self.channel, ', '.join(infos))

    def run(self):
        self.ipinfo()
