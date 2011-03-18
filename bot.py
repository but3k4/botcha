#! /usr/bin/env python2.6
#  -*- coding: latin-1 -*-
#
from ircbot import SingleServerIRCBot
from irclib import nm_to_h, nm_to_n, nm_to_u, nm_to_uh, is_channel, irc_lower, parse_channel_modes
from ConfigParser import ConfigParser
from time import sleep, time, mktime, ctime
from datetime import datetime
import sys, os
import urllib

PATH = os.path.dirname(os.path.abspath(__file__))

reload(sys) 
sys.setdefaultencoding('latin-1')
sys.path.append(os.path.join(PATH, 'modules'))

from search import Search
from daemonize import Daemonize
from database import Database
from logger import Logger
from hashes import Hashes
from convert import Convert
from gtalk import Gtalk

class Decorator(object):
    @classmethod
    def need_op(self, met):
        print "method name = %s" % met.__name__
        def op(*args, **kwargs):
            args[0].conn.privmsg('chanserv', 'op %s %s' % (args[0].channel, args[0].nickname))
            sleep(0.5)
            met(*args, **kwargs)
            args[0].conn.privmsg('chanserv', 'deop %s %s' % (args[0].channel, args[0].nickname))
        return op

class Bot(SingleServerIRCBot):

    log = Logger()
    msglist = []
    qtde_cmd = 3

    def __init__(self, channel, nickname, password, server, port=6667):
        self.nickname = nickname
        self.password = password
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname, reconnection_interval=60)
        self.channel = channel
        self.conn = self.connection
        self.start()

    def connected_checker(self):
        if not self.conn.is_connected():
            self.conn.execute_delayed(self.reconnection_interval, self.connected_checker)
            if self.conn.is_connected(): self.conn.quit("bye")
            self.start()

    def on_join(self, c, e):
        nick = nm_to_n(e.source())
        userhost = nm_to_uh(e.source())
        greeting = self.get_join_msg(nick)
        if greeting: c.privmsg(self.channel, greeting)
        self.log('%s [%s] has joined %s' % (nick, userhost, self.channel))

    def on_quit(self, c, e):
        nick = nm_to_n(e.source())
        userhost = nm_to_uh(e.source())
        msg = self.get_quit_msg(nick)
        if msg: c.privmsg(self.channel, msg)
        self.log('%s [%s] has quit %s' % (nick, userhost, self.channel))

    def on_part(self, c, e):
        nick = nm_to_n(e.source())
        userhost = nm_to_uh(e.source())
        msg = self.get_quit_msg(nick)
        if msg: c.privmsg(self.channel, msg)
        self.log('%s [%s] has left %s' % (nick, userhost, self.channel))

    def on_kick(self, c, e):
        nick = nm_to_n(e.source())
        kicked = e.arguments()[0]
        self.log('%s was kicked off %s by %s' % (kicked, self.channel, nick))
        if kicked == self.nickname:
            sleep(0.5)
            c.privmsg('chanserv', 'unban %s' % self.channel)
            c.privmsg('chanserv', 'akick %s del %s' % (self.channel, self.nickname))
            c.join(self.channel)
            self.kick(nick, 'vai dar kick na puta da sua mae seu miseravel')

    def check_admin(self, n):
        db = Database()
        admin = db.get_value('admin', 'admins', 'admin', n)
        db.disconect()
        return admin

    def get_join_msg(self, n):
        db = Database()
        msg = db.get_value('message', 'join_msg', 'nick', n)
        db.disconect()
        return msg

    def get_quit_msg(self, n):
        db = Database()
        msg = db.get_value('message', 'quit_msg', 'nick', n)
        db.disconect()
        return msg

    def check_user(self, n):
        for ch in self.channels.values():
            if ch.has_user(n): return n

    def on_welcome(self, c, e):
        self.conn.privmsg('NickServ', 'IDENTIFY %s' % self.password)
        sleep(0.5)
        c.privmsg('chanserv', 'unban %s' % self.channel)
        c.privmsg('chanserv', 'akick %s del %s' % (self.channel, self.nickname))
        sleep(0.5)
        c.join(self.channel)
        sleep(0.5)
        c.privmsg('chanserv', 'set flood_protection off')

    def on_privmsg(self, c, e):
        args = e.arguments()[0]
        self.do_command(e, args)

    def on_pubmsg(self, c, e):
        args = e.arguments()[0]
        self.do_command(e, args)

    def xingamento(self, n):
        db = Database()
        xingamento = db.get_random('msg', 'messages')
        db.disconect()
        if xingamento == "Error":
            return "nao existe xingamentos na base, adicione algum que seja construtivo seu arrombado"
        else:
            return n + ', ' + xingamento

    @Decorator.need_op
    def kick(self, n, msg="vaza fela da puta"):
        self.conn.kick(self.channel, n, msg)

    @Decorator.need_op
    def akick(self, n):
        self.conn.privmsg('chanserv', 'akick %s add %s' % (self.channel, n))

    @Decorator.need_op
    def unakick(self, n):
        self.conn.privmsg('chanserv', 'akick %s del %s' % (self.channel, n))

    @Decorator.need_op
    def ban(self, n, msg="eu avisei"):
        self.conn.send_raw("MODE %s +b %s" % (self.channel, n))

    @Decorator.need_op
    def unban(self, n):
        self.conn.send_raw("MODE %s -b %s" % (self.channel, n))

    def anti_flood(self, n, args):
        cmd = args.split(' ')[0]
        timestamp = mktime(datetime.fromtimestamp(time()).timetuple())
        self.msglist.append(str(timestamp) + " " + n.lower() + " " + cmd)
        if len(self.msglist) >= 200:
            del self.msglist[0]

    def count_cmd(self, e, n, command):
        stime = mktime(datetime.fromtimestamp(time()).timetuple()) - 60
        ltime = mktime(datetime.fromtimestamp(time()).timetuple()) - 15
        count = 0
        ncount = 0
        for line in self.msglist:
            tt, nn, cc = line.split(' ')
            if line.find(n.lower()) != -1 and line.find(command) != -1:
                if float(tt) > stime: count += 1
                if float(tt) > ltime: ncount += 1

        if self.check_user(n) and count == 2:
            if is_channel(e.target()):
                self.conn.privmsg(self.channel, '%s larga mao de flood, vai levar kick' % n)
            else:
                self.conn.privmsg(n, 'larga mao de flood, vai levar kick')
        elif self.check_user(n) and ncount > 1 and count == 3:
            self.kick(n, msg="se continuar vai levar ban")
        elif self.check_user(n) and ncount > 1 and count > 3:
            self.ban(n)
        
        return count

    def do_command(self, e, args):
        nick = nm_to_n(e.source())
        user = nm_to_u(e.source()).replace('~', '')
        cmd = args.strip().split(' ')[0]
        args = args.strip()
        c = self.conn

        if self.check_admin(user) and cmd == "!die":
            self.die('estou indo embora, fui')

        elif self.check_admin(user) and cmd == "!join":
            c.join(self.channel)

        elif cmd == '!add_xingamento':
            content = args.strip().replace('!add_xingamento', '')
            if self.count_cmd(e, nick, cmd) < 2:
                if re.compile('b(.*).t(.*).[ck].(.*)', re.I).search(content):
                    self.kick(nick, 'este tipo de xingamento nao eh apropriado')
                elif len(content) > 3:
                    db = Database()
                    try:
                        x_add = db.add('messages', content)
                        db.disconect()
                        if x_add == -1:
                            c.privmsg(self.channel, '%s vai fazer sql injection na puta que pariu' % nick)
                        else:
                            c.privmsg(self.channel, '%s xingamento adicionado com sucesso' % nick)
                    except:
                            c.privmsg(self.channel, '%s nao consegui adicionar seu xingamento, verifique a codificacao que voce esta usando' % nick)

        elif cmd == '!add_quote':
            content = args.strip().replace('!add_quote', '')
            if self.count_cmd(e, nick, cmd) < 2:
                if len(content) > 3:
                    db = Database()
                    try:
                        x_add = db.add('quotes', content)
                        db.disconect()
                        if x_add == -1:
                            c.privmsg(self.channel, '%s vai fazer sql injection na puta que pariu' % nick)
                        else:
                            c.privmsg(self.channel, '%s quote adicionado com sucesso' % nick)
                    except:
                            c.privmsg(self.channel, '%s nao consegui adicionar seu quote, verifique a codificacao que voce esta usando' % nick)

        elif cmd == '!add_gtalk':
            content = args.strip().replace('!add_gtalk', '').split(' ')
            if len(content) == 3:
                if content[2].find('@gmail.com') != -1:
                    db = Database()
                    try:
                        g_add = db.add_gtalk(content[1], content[2])
                        db.disconect()
                        if g_add == -1:
                            c.privmsg(self.channel, '%s vai fazer sql injection na puta que pariu' % nick)
                        else:
                            c.privmsg(self.channel, '%s gtalk adicionado com sucesso' % nick)
                    except:
                            c.privmsg(self.channel, '%s ja existe um gtalk com este nick' % nick)
                else:
                    c.privmsg(self.channel, '%s resuma-se a usar somente: !add_gtalk nick usuario@gmail.com' % nick)

        elif cmd == '!gtalk':
            gcontent = args.replace('!gtalk', '').split(' ')
            gnick = gcontent[1]
            if gnick.isalnum():
                db = Database()
                gemail = db.get_value('gtalk', 'gtalk', 'nick', gnick)
                if not gemail:
                    c.privmsg(self.channel, '%s seu fela da puta, nao existe gtalk cadastrado com esse nick, use: !add_gtalk %s conta@gmail.com' % (nick, gnick))
                else:
                    gmessage = ' '.join(gcontent[2:])
                    gtalk = Gtalk('lokky.b@gmail.com', '')
                    send = gtalk.send(gemail, gmessage)
                    gtalk.disconnect()
                    if not send:
                        c.privmsg(self.channel, '%s mensagem enviada' % nick)
                    else:
                        c.privmsg(self.channel, '%s problemas no envio da mensagem' % nick)
            else:
                c.privmsg(self.channel, '%s arrombado, nick tem que ser alfanumerico' % nick)

        elif cmd == '!vadio' or cmd == '!lero':
            if self.count_cmd(e, nick, cmd) < self.qtde_cmd:
                c.privmsg(self.channel, self.xingamento('lero'))

        elif cmd == '!quote':
            if self.count_cmd(e, nick, cmd) < 2:
                _db = Database()
                quote = _db.get_random('quote', 'quotes')
                _db.disconect()
                c.privmsg(self.channel, quote)

        elif cmd == '!xinga':
            if self.count_cmd(e, nick, cmd) < 2:
                preto = args.replace('!xinga', '').strip()
                if preto.lower() == self.nickname:
                    c.privmsg(self.channel, '%s voce acha que sou idiota a ponto de me xingar?' % nick)
                elif self.check_user(preto):
                    c.privmsg(self.channel, self.xingamento(preto))
                else:
                    c.privmsg(self.channel, '%s deixa de ser idiota e pelo menos xinga alguem do canal' % nick)

        elif cmd == '!vaza':
            if self.count_cmd(e, nick, cmd) < self.qtde_cmd:
                try:
                    preto = args.split(' ')[1]
                    if preto.lower() == self.nickname:
                        c.privmsg(self.channel, '%s voce acha que sou idiota a ponto de me kickar?' % nick)
                    elif self.check_user(preto):
                        self.kick(preto)
                    else:
                        c.privmsg(self.channel, '%s deixa de ser idiota e pelo menos tenta kickar alguem do canal' % nick)
                except:
                        c.privmsg(self.channel, '%s deixa de ser idiota e pelo menos tenta kickar alguem do canal' % nick)

        elif self.check_admin(user) and cmd == "!ban":
            if self.count_cmd(e, nick, cmd) < self.qtde_cmd:
                preto = args.split(' ')[1]
                if preto.lower() == self.nickname:
                    c.privmsg(self.channel, '%s voce acha que sou idiota a ponto de me banir?' % nick)
                elif self.check_user(preto):
                    c.privmsg(self.channel, '%s Asta la Vista, baby!' % preto)
                    sleep(2)
                    self.ban(preto, 'some fela da puta')
                else:
                    c.privmsg(self.channel, '%s deixa de ser idiota e pelo menos tenta banir alguem do canal' % nick)

        elif self.check_admin(user) and cmd == "!unban":
            if self.count_cmd(e, nick, cmd) < self.qtde_cmd:
                preto = args.split(' ')[1]
                if preto.lower() == self.nickname:
                    c.privmsg(self.channel, '%s eu nao estou banido seu idiota' % nick)
                else:
                    self.unban(preto)

        elif self.check_admin(user) and cmd == "!akick":
            if self.count_cmd(e, nick, cmd) < self.qtde_cmd:
                preto = args.split(' ')[1]
                if preto.lower() == self.nickname:
                    c.privmsg(self.channel, '%s voce acha que sou idiota a ponto de colocar meu nick na akick?' % nick)
                elif self.check_user(preto):
                    c.privmsg(self.channel, '%s Se fodeu :)' % preto)
                    sleep(2)
                    self.akick(preto)
                else:
                    c.privmsg(self.channel, '%s deixa de ser idiota e informa o nick de alguem do canal seu retardado' % nick)

        elif self.check_admin(user) and cmd == "!unakick":
            if self.count_cmd(e, nick, cmd) < self.qtde_cmd:
                preto = args.split(' ')[1]
                if preto.lower() == self.nickname:
                    c.privmsg(self.channel, '%s eu nao estou na akick seu idiota' % nick)
                else:
                    self.unakick(preto)

        elif cmd == '!flambers':
            if self.count_cmd(e, nick, cmd) < self.qtde_cmd:
                c.privmsg(self.channel, 'flambers, cadê a maconha seu safado?')

        elif cmd == '!brigadeiro':
            if self.count_cmd(e, nick, cmd) < self.qtde_cmd:
                bpreto = args.replace('!brigadeiro', '').strip()
                if bpreto:
                    c.privmsg(self.channel, '%s voce ta pegando so um brigadeiro? voce so pode pegar um hein?' % bpreto)
                else:
                    c.privmsg(self.channel, 'ja avisei todos voces, so pode pegar um brigadeiro.')

        elif cmd == '!wow':
            if self.count_cmd(e, nick, cmd) < self.qtde_cmd:
                wpreto = args.replace('!wow', '').strip()
                if wpreto:
                    c.privmsg(self.channel, '%s vamos fazer uma dungeon?' % wpreto)
                else:
                    c.privmsg(self.channel, 'alguem aqui do canal ta afim de fazer uma dungeon?')

        elif cmd == '!md5':
            if self.count_cmd(e, nick, cmd) < 2:
                string = args.strip().replace('!md5', '').strip()
                if (len(string) >= 1):
                    md5 = Hashes()
                    result = md5.md5(string)
                    c.privmsg(self.channel, 'md5: ' + result)
                else:
                    c.privmsg(self.channel, '%s gerar md5 de nenhum caracter eh foda hein?' % nick)

        elif cmd == '!crypt':
            if self.count_cmd(e, nick, cmd) < 2:
                string = args.strip().replace('!crypt', '').strip()
                if (len(string) >= 1):
                    crypt = Hashes()
                    result = crypt.crypt(string)
                    c.privmsg(self.channel, 'crypt: ' + result)
                else:
                    c.privmsg(self.channel, '%s gerar crypt de nenhum caracter eh foda hein?' % nick)

        elif cmd == '!tbinary':
            if self.count_cmd(e, nick, cmd) < 2:
                string = args.strip().replace('!tbinary', '').strip()
                if (len(string) >= 1):
                    binary = Convert()
                    result = binary.string2binary(string)
                    c.privmsg(self.channel, 'to binary: ' + result)
                else:
                    c.privmsg(self.channel, '%s gerar binario sem caracter algum eh foda hein?' % nick)

        elif cmd == '!fbinary':
            if self.count_cmd(e, nick, cmd) < 2:
                binary = args.strip().replace('!fbinary', '').strip()
                if (len(binary) > 1):
                    string = Convert()
                    result = string.binary2string(binary)
                    c.privmsg(self.channel, 'from binary: ' + result)
                else:
                    c.privmsg(self.channel, '%s informe algum caracter binario seu idiota?' % nick)

        elif cmd == '!google':
            search = Search()
            string = args.strip().replace('!google', '').strip().replace(':', ' ')
            if self.count_cmd(e, nick, cmd) < 2:
                if (len(string) >= 3):
                    for result in search.google(string):
                        c.privmsg(self.channel, result)
                        sleep(2)
                else:
                    c.privmsg(self.channel, '%s utilize pelo menos 3 letras na sua pesquisa seu retardado' % nick)

        elif cmd == '!transito':
            search = Search()
            string = args.strip().replace('!transito', '').strip().replace(':', ' ')
            if self.count_cmd(e, nick, cmd) < 2:
                try:
                    result = search.maplink()
                    c.privmsg(self.channel, result.strip())
                    sleep(2)
                except:
                    c.privmsg(self.channel, '%s problemas ao acessar o site da cet, tente novamente mais tarde' % nick)

        elif cmd == '!tinyurl':
            string = args.strip().replace('!tinyurl', '').strip()
            if self.count_cmd(e, nick, cmd) < 2:
                if string.find('http://') != -1:
                        result = urllib.urlopen("http://tinyurl.com/api-create.php?url=%s" % string).read()
                        c.privmsg(self.channel, 'tinyurl: ' + result)
                        sleep(2)
                else:
                    c.privmsg(self.channel, '%s voce eh tao idiota que nao sabe que url tem o http:// ?' % nick)

        elif cmd == '!youtube':
            search = Search()
            string = args.strip().replace('!youtube', '').strip()
            if self.count_cmd(e, nick, cmd) < 2:
                if (len(string) > 0):
                    for result in search.youtube(string):
                        c.privmsg(self.channel, result)
                        sleep(2)
                else:
                    c.privmsg(self.channel, '%s utilize pelo menos 3 letras na sua pesquisa seu retardado' % nick)

        elif cmd == '!help':
            if self.count_cmd(e, nick, cmd) < 2:
                commands = { 'add_xingamento' : 'adiciona xingamentos', 'vadio' : 'xinga o guilherme', 'lero' : 'tambem xinga o guilherme', 'xinga' : 'xinga algum individuo do canal', 'flambers' : 'faz uma pergunta muito importante ao flambers', 'md5' : 'gera hash em md5', 'crypt' : 'gera hash em cript que pode ser usado em qualquer sistema de autenticacao, ex: shadow', 'tbinary' : 'converte de string para binario', 'fbinary' : 'converte de binario para string', 'google' : 'faz pesquisas no google', 'youtube' : 'faz pesquisas no youtube', 'vaza' : 'da um kick em alguem', 'gtalk' : 'envia mensagem pros negos do gtalk (nao esquecer de informar gtalk e mensagem)', 'brigadeiro' : 'pergunta pro nego sobre o brigadeiro', 'wow' : 'chama um nego pra fazer uma dungeon' }
                c.privmsg(nick, 'os comandos disponiveis sao:')
                for x in (commands.keys()):
                    c.privmsg(nick, '%s: %s' % (x, commands[x]))
                    sleep(1)

        if is_channel(e.target()):
            self.log(self.channel + ": " + nick + " - " + args)
            self.anti_flood(nick, args)
        else:
            self.log('pvt' + ": " + nick + " - " + args)
            self.anti_flood(nick, args)

if __name__ == "__main__":
    daemon = Daemonize(os.path.join(PATH, 'startup.log'))
    daemon.start()
    config = ConfigParser()
    section = 'lokky'
    config.read(os.path.join(PATH, 'conf/config.cfg'))
    channel = config.get(section, 'channel')
    nick = config.get(section, 'nickname')
    passwd = config.get(section, 'password')
    network = config.get(section, 'network')

    bot = Bot(channel, nick, passwd, network)
    bot.connected_checker()

    sys.stdout.write('lokky started with pid %d\n' % os.getpid())
