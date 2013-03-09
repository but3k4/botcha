#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import Web
import random
import re

class Sl(Base_Command.Base_Command):

    def sl(self):
        user = 'iLikeGirlsDaily'
        number = 60
        web = Web()
        try:
            answer = web.json(web.get("http://search.twitter.com/search.json?q=@%s&rpp=%s&include_entities=true&result_type=recent" % (user, number)))
            pattern = re.compile('(\'media_url\':\s?u\')(http://[^\s]+)\'')
            result = []
            [ result.append(line[1]) for line in re.findall(pattern, str(answer)) if not line[1] in result ]
            self.parent.conn.privmsg(self.channel, random.choice(result))
        except:
            return False

    def run(self):
        self.sl()
