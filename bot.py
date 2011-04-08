#! /usr/bin/env python
#  -*- coding: latin-1 -*-
#
from ircbot import SingleServerIRCBot
from irclib import nm_to_h, nm_to_n, nm_to_u, nm_to_uh, is_channel
from ConfigParser import ConfigParser
from time import sleep, time
from imp import load_source
import sys, os

PATH = os.path.dirname(os.path.abspath(__file__))

reload(sys)
sys.setdefaultencoding('latin-1')
sys.path.append(os.path.join(PATH, 'modules'))

from logger import Logger
from daemonize import Daemonize

class Commands(object):

    commands = {}

    def __init__(self, parent, cmd, event):
        self.parent = parent
        self.cmd = cmd.strip('!')
        self.event = event

        for command in os.listdir(os.path.join(PATH, 'commands')):
            if command.endswith('.py'):
                name = command.strip('.py')
                self.commands[name] = load_source(name, os.path.join(PATH, 'commands', command))

    def run(self):
        if self.cmd in self.commands:
            obj = getattr(self.commands[self.cmd], self.cmd.capitalize())(self.parent, self.event)
            obj.run()

class Bot(SingleServerIRCBot):

    log = Logger()
    
    def __init__(self, channel, nickname, password, server, port=6667):
        self.nickname = nickname
        self.password = password
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname, reconnection_interval=60, ipv6=True)
        self.channel = channel
        self.conn = self.connection
        self.start()

    def on_join(self, c, e):
        nick = nm_to_n(e.source())
        host = nm_to_uh(e.source())
        self.log('%s [%s] has joined %s' % (nick, host, self.channel))

    def on_quit(self, c, e):
        nick = nm_to_n(e.source())
        host = nm_to_uh(e.source())
        self.log('%s [%s] has quit %s' % (nick, host, self.channel))

    def on_part(self, c, e):
        nick = nm_to_n(e.source())
        host = nm_to_uh(e.source())
        self.log('%s [%s] has left %s' % (nick, host, self.channel))

    def on_kick(self, c, e):
        nick = nm_to_n(e.source())
        kicked = e.arguments()[0]
        self.log('%s was kicked off %s by %s' % (kicked, self.channel, nick))

    def on_welcome(self, c, e):
        c.privmsg('NickServ', 'IDENTIFY %s' % self.password)
        c.join(self.channel)
        c.privmsg('chanserv', 'set flood_protection off')

    def on_privmsg(self, c, e):
        self.do_command(c, e)

    def on_pubmsg(self, c, e):
        self.do_command(c, e)

    def do_command(self, c, e):
        message = e.arguments()[0]
        cmd = message.strip().split()[0]
        nick = nm_to_n(e.source())

        if cmd.startswith('!'):
            command = Commands(self, cmd, e)
            command.run()

        if is_channel(e.target()):
            self.log('%s: %s - %s' % (self.channel, nick, message))
        else:
            self.log('pvt: %s - %s' % (nick, message))

if __name__ == "__main__":
    daemon = Daemonize(os.path.join(PATH, 'startup.log'))
    daemon.start()
    config = ConfigParser()
    config.read(os.path.join(PATH, 'conf/config.cfg'))
    channel = config.get('lokky', 'channel')
    nick = config.get('lokky', 'nickname')
    passwd = config.get('lokky', 'password')
    network = config.get('lokky', 'network')

    bot = Bot(channel, nick, passwd, network)
