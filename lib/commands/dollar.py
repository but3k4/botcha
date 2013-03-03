#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import Web

class Dollar(Base_Command.Base_Command):

    def get_text(self, nodelist):
        r = [ node.data for node in nodelist if node.nodeType == node.TEXT_NODE ]
        return ''.join(r)

    def dollar(self):
        url = 'http://www4.bcb.gov.br/feed/taxas.ashx'
        web = Web()
        result = web.xml(web.get(url))

        if result:

            for element in result.getElementsByTagName("item"):
                title = self.get_text(element.getElementsByTagName("title")[0].childNodes)
                description = self.get_text(element.getElementsByTagName("description")[0].childNodes)
                if str(title).endswith('EUA'):
                    data = "%s %s" % (title, ' '.join(web.html(description).findAll('div', id='value', text=True)))

            data += ', fonte: www.bcb.gov.br'
            self.parent.conn.privmsg(self.channel, '%s, %s' % (self.nick, data.lower().replace('&agrave;', 'à')))

    def run(self):
        self.dollar()
