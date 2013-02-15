from irclib import nm_to_n, nm_to_u
from lib.modules.database import Database

class Base_Command(object):
    def __init__(self, parent, event):
        self.args = event.arguments()[0].split()[1:]
        self.parent = parent
        self.target = nm_to_n(event.source())
        self.nick = nm_to_u(event.source()).strip('~')
        self.channel = event.target()
        self.__setup__()

    def check_admin(self):
        db = Database()
        self.nick = None
        try:
            self.nick = db.select('admin', 'admins')
            print "admin nick = %s" % self.nick
            print type(self.nick)
        except:
            return False
        return self.nick

    def __setup__(self):
        pass
