import os
import curses
from threading import Thread
import threading

class CursesUI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)
        curses.noecho()
        curses.cbreak()
        self.should_run_lock = threading.Lock()
        self.should_run = True
        self.running = False

    def run(self):
        while True:
            c = self.stdscr.getch()
            if c == ord('q'): break
        self.end_curses()

    def refresh(self):
        # Main loop
        # show 5 most recent messages
        self.stdscr.addstr('x')
        self.stdscr.refresh()

    def end_curses(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def set_message_list(self, list):
        self.msg_list = list

    def set_should_run_synced(self, newval):
        self.should_run_lock.acquire()
        self.should_run = False
        self.should_run_lock.release()

    def stop(self):
        if self.running:
            #print 'stopping ui'
            self.set_should_run_synced(False)
