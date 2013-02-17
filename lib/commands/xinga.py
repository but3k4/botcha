#  -*- coding: utf-8 -*-
#
from lib.commands import Base_Command
from lib.modules.database import Database
from irclib import nm_to_n

class Xinga(Base_Command.Base_Command):

    def xinga(self,e):
	nick = nm_to_n(e.source())	
	if len(self.args) < 1:
		self.parent.conn.privmsg(self.channel,'%s, deixa de ser burro e xinga alguém. ' % nick)	
	else:
	        db = Database()
	        self.xinga = None
	        try:
	        	self.xinga = db.select('xinga', 'xingamentos', 1)[0][0]
	        except:
	            	return False
	        if self.xinga:
	            	self.parent.conn.privmsg(self.channel,'%s, %s' % (self.args[0],self.xinga))

    def run(self, e):
        self.xinga(e)
