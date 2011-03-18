#  -*- coding: latin-1 -*-
#
"""
gtalk.py - lokky gtalk module
Copyright 2009, Claudio Borges
Licensed under BSD License.
"""
import xmpp, sys

class Gtalk(object):
    
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.jid = xmpp.protocol.JID(user)
        self.client = xmpp.Client(self.jid.getDomain(), debug=[])
        self.connect()
        self.auth()

    def connect(self):
        if not self.client.connect():
            print "Error connecting to talk.google.com"
            sys.exit(1)

    def auth(self):
        if not self.client.auth(self.jid.getNode(), self.pwd, resource=self.jid.getResource()):
            raise "Error authenticating to talk.google.com"
            sys.exit(1)

    def send(self, jid, msg):
        self.client.send(xmpp.Presence(to=jid, typ='subscribed'))
        self.client.send(xmpp.Presence(to=jid, typ='subscribe'))
        if not self.client.send(xmpp.protocol.Message(jid, msg)):
            raise "Error sending message to %s" % jid

    def disconnect(self):
        try:
            self.client.disconnect()
        except:
            raise "Disconnect problems"
