CREATE TABLE admins (id INTEGER PRIMARY KEY, admin VARCHAR);
CREATE TABLE akick (id INTEGER PRIMARY KEY, user VARCHAR);
CREATE TABLE gtalk(nick VARCHAR PRIMARY KEY, gtalk VARCHAR);
CREATE TABLE join_msg(id integer primary key, nick varchar, message varchar);
CREATE TABLE quit_msg(id integer primary key, nick varchar, message varchar);
CREATE TABLE quotes (id INTEGER PRIMARY KEY, quote VARCHAR);
CREATE TABLE xingamentos(id INTEGER PRIMARY KEY, msg VARCHAR);
