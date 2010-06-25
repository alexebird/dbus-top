import os
import curses
from common.evented_thread import EventedThread

class CursesUIThread(EventedThread):
    def __init__(self):
        EventedThread.__init__(self, 'CursesUIThread')
        self.message_q = None

    def do_run(self):
        curses.wrapper(self.__do_run)

    def __do_run(self, stdscr):
        self.stdscr = stdscr
        self.refresh()
        while self.should_run:
            c = self.stdscr.getkey()
            self.fire_event('key_pressed', c)

    def add_key_pressed_callback(self, method):
        self.add_callback('key_pressed', method)

    def refresh(self):
        rows = self.stdscr.getmaxyx()[0]
        num_msgs = len(self.message_q)
        if -rows < -num_msgs:
            first_row_index = -num_msgs
        else:
            first_row_index = -rows
        lines = self.message_q[first_row_index:-1]
        for i in range(len(lines)):
            self.stdscr.addstr(i, 0, lines[i].to_string())
        self.stdscr.move(rows-1, 0)
        self.stdscr.refresh()
