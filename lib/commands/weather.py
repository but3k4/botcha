#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.web import Web
import time
import datetime

class Weather(Base_Command.Base_Command):

    def weather(self):
        if len(self.args) < 1:
            place = 'sao paulo sp brazil'
        else:
            place = ' '.join(self.args[0:])

        if 'inferno' in place:
            date = datetime.datetime.now().strftime("BR at %H:00 %p BRT")
            self.parent.conn.privmsg(self.channel, "Conditions for %s, %s: Fair, 666 °C, high: 999 °C, low: 66 °C" % (place.capitalize(), date))

        try:
            web = Web()
            url = 'http://query.yahooapis.com/v1/public/yql'
            query = web.encode({'q': 'select item from weather.forecast where woeid in (select woeid from geo.places where text="%s") and u="c"' % place})
            response = web.json(web.get("%s?%s&format=json&callback=" % (url, query)))
            try:
                data = response["query"]["results"]["channel"][0]['item']
            except:
                data = response["query"]["results"]["channel"]['item']
            infos = {
                'place': data['title'],
                'temperature': data['condition']['temp'],
                'condition': data['condition']['text'],
                'high': data['forecast'][0]['high'],
                'low': data['forecast'][0]['low'],
                }

            result = "%(place)s: %(condition)s, %(temperature)s °C, high: %(high)s °C, low: %(low)s °C" % infos
            self.parent.conn.privmsg(self.channel, result)
        except:
            return False

    def run(self):
        self.weather()
