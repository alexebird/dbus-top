import os
import curses
from evented_thread import EventedThread

class CursesUIThread(EventedThread):
    def __init__(self):
        EventedThread.__init__(self, 'CursesUIThread')

    def do_run(self):
        curses.wrapper(self.__run_curses)

    def __run_curses(self, stdscr):
        self.stdscr = stdscr
        while self.should_run:
            c = self.stdscr.getkey()
            self.fire_event('key_pressed', c)

    #def set_message_list(self, list):
        #self.msg_list = list

    def add_key_pressed_callback(self, method):
        self.add_callback('key_pressed', method)

    def refresh(self):
        self.stdscr.refresh()

    def print_str(self, c):
        self.stdscr.addstr(c)
        self.refresh()
