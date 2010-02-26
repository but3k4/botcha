#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
"""
database.py - lokky database module
Copyright 2008, Claudio Borges
Licensed under BSD License.
"""
import sqlite3 as sqlite
import re
from types import *

class Database(object):

    def __init__(self, db='db/sqlite.db'):
        self.conn = sqlite.connect(db)
        self.cursor = self.conn.cursor()

    def add(self, table, content):
        content = content.strip()
        invalid = [ 'select', 'drop', 'insert', '[\`\']' ]
        injection = None
        for value in invalid:
            if re.compile(value, re.I).search(content):
                injection = 1
                break

        if not injection:
            sql = "INSERT INTO %s VALUES (NULL, '%s')" % (table, content)
            self.cursor.execute(sql)
            self.conn.commit()
        else:
            return -1

    def add_gtalk(self, content1, content2):
        content1 = content1.strip()
        content2 = content2.strip()
        invalid = [ 'select', 'drop', 'insert', '[\`\']' ]
        injection = None
        for value in invalid:
            if re.compile(value, re.I).search(content1) or re.compile(value, re.I).search(content2):
                injection = 1
                break

        if not injection:
            sql = "INSERT INTO gtalk VALUES ('%s', '%s')" % (content1, content2)
            self.cursor.execute(sql)
            self.conn.commit()
        else:
            return -1

    def get_random(self, field, table):
        self.cursor.execute("SELECT %s FROM %s ORDER BY random() LIMIT 1" % (field, table))
	try:
        	result = self.cursor.fetchone()[0]
	except:
		result = "Error"
        return result

    def get_value(self, field1, table, field2, nick=None):
        if nick != None:
            self.cursor.execute("SELECT %s FROM %s WHERE %s = '%s'" % (field1, table, field2, nick))
            result = self.cursor.fetchone()
            if type(result) is not NoneType:
                return result[0]

    def disconect(self):
        self.cursor.close()
        self.conn.close()
