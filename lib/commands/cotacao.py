#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import Web
import re
import types

class Cotacao(Base_Command.Base_Command):

    def cotacao(self):
        url = 'http://economia.uol.com.br/cotacoes'
        web = Web()
        response = web.html(web.get(url))
        result = []
        infos = {}

        if len(self.args) < 1:
            exchange = None
        else:
            exchange = self.args[0]

        regex = {
            'dolar turismo': [ r'(d.lar\stur.)\n.ompra\s+(?P<compra>.+)\n.enda\s+(?P<venda>.+)' ],
            'dolar comercial': [ r'(d.lar\scom.)\n.ompra\s+(?P<compra>.+)\n.enda\s+(?P<venda>.+)', r'(d.lar\s.omercial)\n(?P<compra>.+)\n(?P<venda>.+)' ],
            'euro': [ r'(euro)\n.ompra\s+(?P<compra>.+)\n.enda\s+(?P<venda>.+)', r'(euro)\n(?P<compra>.+)\n(?P<venda>.+)' ],
            'libra': [ r'(libra)\n.ompra\s+(?P<compra>.+)\n.enda\s+(?P<venda>.+)', r'(libra)\n(?P<compra>.+)\n(?P<venda>.+)' ],
        }

        if response:
            try:
                for k, v in regex.iteritems():
                    for l in v:
                        r = re.compile(l, re.I).search(response.text)
                        if not isinstance(r, types.NoneType):
                            if k not in infos:
                                infos[k] = "compra = %s, venda = %s" % (r.group(2).replace(',', '.'), r.group(3).replace(',', '.'))

                if exchange:
                    for k, v in infos.iteritems():
                        if exchange in k:
                            result.append("%s: %s, " % (k, v))
                else:
                    for k, v in infos.iteritems():
                        result.append("%s: %s, " % (k, v))

                if result:
                    result.append('fonte: %s' % url.split('/')[2])
                    self.parent.conn.privmsg(self.channel, '%s, %s' % (self.nick, ''.join(result)))
            except:
                return False

    def run(self):
        self.cotacao()
