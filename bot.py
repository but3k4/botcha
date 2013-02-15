#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
import gevent.monkey
gevent.monkey.patch_all()

import os
import sys
import struct
import time

import lib.commands

from imp import load_source
from ConfigParser import ConfigParser

from ircbot import SingleServerIRCBot
from irclib import nm_to_h, nm_to_n, nm_to_u, nm_to_uh, is_channel

from lib.modules.logger import Logger
from lib.modules.daemonize import Daemonize

reload(sys)
sys.setdefaultencoding('utf-8')

#__import__('irclib').DEBUG = True

class Commands(object):
    commands = {}
    def __init__(self, parent, cmd, event):
        self.parent = parent
        self.cmd = cmd.strip('!')
        self.event = event
        for command in os.listdir(lib.commands.__file__.rsplit("/", 1)[0]):
            if command.endswith('.py') and command not in ['__init__.py', 'Base_Command.py']:
                name = command.rstrip('.py')
                self.commands[name] = load_source(name, os.path.join(lib.commands.__file__.rsplit("/", 1)[0], command))

    def run(self):
        if self.cmd in self.commands:
            obj = getattr(self.commands[self.cmd], self.cmd.capitalize())(self.parent, self.event)
            obj.run()

class Bot(SingleServerIRCBot):

    def __init__(self, channel, nickname, password, server, port=6667):
        self.dcc_received = {}
        self.nickname = nickname
        self.password = password
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname, reconnection_interval=60, ipv6=True)
        self.channel = channel
        self.conn = self.connection
        self.messages = []
        self.log = Logger()

        self.start()

    def connected_checker(self):
        if not self.conn.is_connected():
            self.start()
        self.conn.execute_delayed(self.reconnection_interval, self.connected_checker, ())

    def on_join(self, c, e):
        nick = nm_to_n(e.source())
        host = nm_to_uh(e.source())
        self.log('%s [%s] has joined %s' % (nick, host, str(self.channel)))

    def on_quit(self, c, e):
        nick = nm_to_n(e.source())
        host = nm_to_uh(e.source())
        self.log('%s [%s] has quit %s' % (nick, host, str(self.channel)))

    def on_part(self, c, e):
        nick = nm_to_n(e.source())
        host = nm_to_uh(e.source())
        self.log('%s [%s] has left %s' % (nick, host, str(self.channel)))

    def on_kick(self, c, e):
        nick = nm_to_n(e.source())
        kicked = e.arguments()[0]
        self.log('%s was kicked off %s by %s' % (kicked, str(self.channel), nick))

    def on_welcome(self, c, e):
        c.privmsg('NickServ', 'IDENTIFY %s' % self.password)
        for channel in self.channel:
            c.join(channel)
        c.privmsg('chanserv', 'set flood_protection off')

    def on_privmsg(self, c, e):
        self.do_command(c, e)

    def on_pubmsg(self, c, e):
        self.do_command(c, e)

    def on_ctcp(self, c, e):
        """Default handler for ctcp events.
        Replies to VERSION and PING requests and relays DCC requests
        to the on_dccchat method.

        ncode: Adding dccreceive support
        """
        if e.arguments()[0] == "VERSION":
            c.ctcp_reply(nm_to_n(e.source()), "VERSION " + self.get_version())
        elif e.arguments()[0] == "PING":
            if len(e.arguments()) > 1:
                c.ctcp_reply(nm_to_n(e.source()), "PING " + e.arguments()[1])
        elif e.arguments()[0] == "DCC" and e.arguments()[1].split(" ", 1)[0] == "CHAT":
            self.on_dccchat(c, e)
        elif e.arguments()[0] == "DCC" and e.arguments()[1].split(" ", 1)[0] == "SEND":
            self.filename = "/tmp/%s" % os.path.basename(args[1])
            if os.path.exists(self.filename):
                print "A file named", self.filename,
                print "already exists. Refusing to save it."
            self.file = open(self.filename, "w")
            peeraddress = irclib.ip_numstr_to_quad(args[2])
            peerport = int(args[3])
            self.dcc = self.dcc_connect(peeraddress, peerport, "raw")

    def on_dccmsg(self, connection, event):
        data = event.arguments()[0]
        self.file.write(data)
        self.received_bytes = self.received_bytes + len(data)
        self.dcc.privmsg(struct.pack("!I", self.received_bytes))

    def on_dcc_disconnect(self, connection, event):
        self.file.close()
        print "Received file %s (%d bytes)." % (self.filename, self.received_bytes)

    def anti_flood(self, nick, cmd):
        curtime = time.mktime(time.gmtime())
        timestamp = curtime - 60
        count = 0
        
        self.messages.append("%f %s %s" % (curtime, nick, cmd))
        if len(self.messages) > 200:
            del self.messages[0]

        for line in self.messages:
            t, n, c = line.split()
            if nick in line and cmd in line and float(t) > timestamp:
                count += 1

        return count

    def do_command(self, c, e):
        message = e.arguments()[0]
        cmd = message.strip().split()[0]
        nick = nm_to_n(e.source())

        if cmd.startswith('!'):
            if self.anti_flood(nick, cmd) >= 4:
                self.conn.privmsg(e.target(), 'flood protection enabled, wait few seconds and try again')
            else:
                command = Commands(self, cmd, e)
                command.run()

        if is_channel(e.target()):
            self.log('%s: %s - %s' % (self.channel, nick, message))
        else:
            self.log('pvt: %s - %s' % (nick, message))

def main():
    config = ConfigParser()
    section = 'lokky'
    try:
        config.read("conf/lokky.cfg")
    except Exception, e:
        self.log("Error while reading the config file: %s" % e) 
        return False
    channel = config.get(section, 'channel').split(',')
    nick = config.get(section, 'nickname')
    passwd = config.get(section, 'password')
    network = config.get(section, 'network')
    port = config.getint(section, 'port')

    bot = Bot(channel, nick, passwd, network, port)

if __name__ == "__main__":
    daemon = Daemonize("log/startup.log")
    daemon.start()
    main()
