from irclib import nm_to_n, nm_to_u
from lib.modules.database import Database

class Base_Command(object):
    def __init__(self, parent, event):
        self.args = event.arguments()[0].split()[1:]
        self.parent = parent
        self.nick = nm_to_n(event.source())
        self.name = nm_to_u(event.source()).strip('~')
        self.channel = event.target()
        self.__setup__()

    def check_admin(self):
        db = Database()
        self.admins = None
        try:
            self.admins = [ nick[0] for nick in db.select('admin', 'admins') ]
        except:
            return False
        return self.name in self.admins

    def __setup__(self):
        pass
