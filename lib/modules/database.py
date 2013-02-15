#  -*- coding: utf-8 -*-
#
"""
database.py - lokky database module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
import sqlite3
import os.path
from types import *

class Database(object):

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 2)[0]
        db = os.path.join(path, 'db/sqlite.db')
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def insert(self, table, value):
        sql = "INSERT INTO %s VALUES (NULL, '%s')" % (table, value)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            return False

    def select(self, field, table, random=0):
        try:
            if random:
                self.cursor.execute("SELECT %s FROM %s ORDER BY random() LIMIT 1" % (field, table))
            else:
                self.cursor.execute("SELECT %s FROM %s" % (field, table))
        except:
            return False

        result = self.cursor.fetchall()
        self.disconect()

        if type(result) is not NoneType:
            return result

    def disconect(self):
        self.cursor.close()
        self.conn.close()
