#  -*- coding: latin-1 -*-
#
"""
database.py - lokky database module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
import sqlite3 as sqlite
from os.path import abspath, dirname, join
from types import *

class Database(object):

    def __init__(self):
        path = '/'.join(dirname(abspath(__file__)).split('/')[:-1])
        dbfile = join(path, 'db/sqlite.db')
        self.conn = sqlite.connect(dbfile)
        self.cursor = self.conn.cursor()

    def add(self, table, content):
        try:
            sql = "INSERT INTO %s VALUES (NULL, '%s')" % (table, content.strip())
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            return -1

    def add_gtalk(self, content1, content2):
        try:
            sql = "INSERT INTO gtalk VALUES ('%s', '%s')" % (content1.strip(), content2.strip())
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            return -1

    def get_random(self, field, table):
        try:
            self.cursor.execute("SELECT %s FROM %s ORDER BY random() LIMIT 1" % (field, table))
            return self.cursor.fetchone()[0]
        except:
            return -1

    def get_value(self, field1, table, field2, nick=None):
        if nick != None:
            try:
                self.cursor.execute("SELECT %s FROM %s WHERE %s = '%s'" % (field1, table, field2, nick))
                result = self.cursor.fetchone()
                if type(result) is not NoneType:
                    return result[0]
            except:
                return -1

    def disconect(self):
        self.cursor.close()
        self.conn.close()
