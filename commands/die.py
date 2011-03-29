#  -*- coding: latin-1 -*-
#
from irclib import nm_to_n, nm_to_u
from database import Database

class Die(object):

    def __init__(self, parent, event):
        self.parent = parent
        self.target = nm_to_n(event.source())
        self.nick = nm_to_u(event.source()).strip('~')
        self.commands = { 'die': 'die' }

    def check_admin(self):
        db = Database()
        user = db.get_value('admin', 'admins', 'admin', self.nick)
        db.disconect()
        if len(user) > 0:
            return True
        return False

    def die(self):
        if self.check_admin():
            self.parent.conn.privmsg(self.parent.channel, 'o %s me mandou ir embora :~' % self.target)
            self.parent.die()

    def run(self):
        self.die()
