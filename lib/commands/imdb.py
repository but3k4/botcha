#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import Web
import types

class Imdb(Base_Command.Base_Command):

    def imdb(self):
        if len(self.args) < 1:
            return False
        else:
            movie = ' '.join(self.args[0:])

        try:
            web = Web()
            movie = movie.replace(' ', '+')
            url = "http://www.imdbapi.com/?t=" + movie
            response = web.json(web.get(url))
            if not isinstance(response, types.NoneType):
                if 'Error' in response:
                    return False
                else:
                    infos = {
                        'title': response['Title'],
                        'year': response['Year'][:4],
                        'genre': response['Genre'],
                        'rating': response['imdbRating'],
                        'url': 'http://imdb.com/title/%s' % response['imdbID'],
                    }

                    result = "%(title)s, genre: %(genre)s, year: %(year)s, rating: %(rating)s, url: %(url)s" % infos
                    self.parent.conn.privmsg(self.channel, result)
        except:
            return False

    def run(self):
        self.imdb()
