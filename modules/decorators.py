#  -*- coding: latin-1 -*-
#
class Decorator(object):

    @classmethod
    def need_op(self, met):
        def op(*args, **kwargs):
            args[0].conn.privmsg('chanserv', 'op %s %s' % (args[0].channel, args[0].nickname))
            met(*args, **kwargs)
            args[0].conn.privmsg('chanserv', 'deop %s %s' % (args[0].channel, args[0].nickname))
        return op
