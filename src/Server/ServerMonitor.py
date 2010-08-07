#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    This file defines ServerMonitor class.
"""

import sys
import time
from threading import Thread

class ServerMonitor(Thread):
    """
        This class defines a class which monitors server.
        It is designed to run in a new thread.
    """
    KW_HELP = ['?','help']
    KW_QUIT = ['quit']
    KEYWORDS = KW_HELP + ['quit', 'detach', 'start','close', 'kill','show pos','show player','show stat']
    def __init__(self, server = None, args = ()):
        Thread.__init__(self)
        self.server = server
        if args:
            #parse arguments
            pass

    def getHelp(self, command = ''):
        HELPMSG = """
Available commands are :
    ? or help   - show help messages
    quit        - quit monitor (leave server open)
    detach      - stop running a server
    start       - start server
    close       - close server
    kill        - stop server
    show pos    - print ChessBoard position data
    show player - print Player data
    show stat   - print server stat data
        """
        STARTMSG = """
            start [port] - Start server, if port is not specified, the default port is specified.
            if server has already been running, this command is ignored.
        """
        SHOWMSG = """
            show pos <pos_num> - print Position data
            show player <ply_id> - print Player id
            show stat - print server running stat

            if server is not run, these commands are ignored.
        """
        if not command:
            self.dbg(HELPMSG)
        elif command == 'start':
            self.dbg(STARTMSG)
        elif command == 'show':
            self.dbg(SHOWMSG)

    def log(self, text):
        #debug and writing into log file
        #log it
        pass

    def dbg(self, text):
        #debug(display) only, not writing into log file
        sys.stdout.write(text)

    def err(self, text):
        #error message, writing into log file
        #log it
        sys.stderr.write(text)

    def getInput(self):
        return raw_input('? ')

    def run(self):
        self.getHelp()
        while 1:
            s = self.input().strip()
            phrase0 = s.split(' ',1)
            if phrase0 in ServerMonitor.KW_HELP:
                self.getHelp(s[len(phrase0):].strip())
            elif phrase0 in ServerMonitor.KW_QUIT:
                break
            # ... why use run() and call() ...
            elif self.call(s)

    def killServer(self):
        if self.server:
            self.closeServer()
            self.detachServer()

    def isRunning(self):
        if not self.server:
            return False
        pass

    def startServer(self, port):
        if self.isRunning():
            break
        if not self.server:
            self.server = GameService(port)
        self.server.setMonitor(self)
        #run server like self.server.run()

    def closeServer(self):
        if self.isRunning():
            self.server.stop()

    def detachServer(self):
        if self.server:
            self.server = None

    def call(self, source):
        source = source.strip()
        if self.server:
            if source.startswith('show data')
            pass
        time.sleep(0)

if __name__=='__main__':
    threads = []
    for i in range(2):
        thread = ServerMonitor()
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print 'main thread exiting'
