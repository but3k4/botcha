#  -*- coding: utf-8 -*-
#
import httplib2
import re 
import random
import json

class Twitterz(object):

    def __init__(self):
        pass

    def get_twipz(self, user, num):
        sock = httplib2.Http(timeout=5)
        headers, response = sock.request("http://search.twitter.com/search.json?q=@%s&rpp=%s&include_entities=true&result_type=recent" % (user, num))
        if headers['status'] in (200, '200'):
            return json.loads(response)

    def get_random_twipz(self, result):
        try:
            return result['results'][random.randint(0, 29)]['entities']['media'][0]['media_url']
        except:
            return False

    def ilikegirlz(self):
        try:
            answer_data = self.get_twipz('iLikeGirlsDaily', 30)
        except:
            return False

        while True:
            ret = self.get_random_twipz(answer_data)
            if ret:
                return ret
