import os
import curses
#import curses.wrapper
import threading
from threading import Thread

class CursesUIThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = 'CursesUIThread'
        #self.stdscr.keypad(1)
        #curses.noecho()
        #curses.cbreak()
        self.should_run_lock = threading.Lock()
        self.should_run = True
        self.running = False
        self.callbacks = {}

    def run(self):
        curses.wrapper(self.__run_curses)

    def __run_curses(self, stdscr):
        self.stdscr = stdscr
        while self.should_run:
            c = self.stdscr.getkey()
            self.__fire_event('key_pressed', c)
        #self.end_curses()

    def refresh(self):
        # Main loop
        # show 5 most recent messages
        self.stdscr.refresh()

    def print_str(self, c):
        self.stdscr.addstr(c)
        self.refresh()

    #def end_curses(self):
        #curses.nocbreak()
        #self.stdscr.keypad(0)
        #curses.echo()
        #curses.endwin()

    def set_message_list(self, list):
        self.msg_list = list

    def set_should_run_synced(self, newval):
        self.should_run_lock.acquire()
        self.should_run = False
        self.should_run_lock.release()

    def stop(self):
        if self.running:
            self.set_should_run_synced(False)

    def add_key_pressed_callback(self, method):
        self.__add_callback('key_pressed', method)

    #
    # General purpose event mechanism methods
    #

    def __add_callback(self, callback_name, method):
        try:
            self.callbacks[callback_name]
        except KeyError:
            self.callbacks[callback_name] = []
        self.callbacks[callback_name].append(method)

    def __fire_event(self, event_name, data):
        for m in self.callbacks[event_name]:
            m(data)
