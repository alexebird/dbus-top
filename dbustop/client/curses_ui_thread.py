import os
import curses
import time
from dbustop.common import util
from dbustop.common.base_thread import BaseThread
from dbustop.common.event.event import Event
from dbustop.common.event import event_handler

class CursesUIThread(BaseThread):
    def __init__(self):
        BaseThread.__init__(self, 'CursesUIThread')
        self.data_model = []

    def run(self):
        curses.wrapper(self.__run)

    def __run(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.nodelay(1)
        self.refresh()
        while self.should_run():
            try:
                c = self.stdscr.getkey()
                event_handler.add_event(Event(self.name, 'key_pressed', c))
            except curses.error:
                pass
            time.sleep(0.1)

    def refresh(self):
        rows = self.stdscr.getmaxyx()[0]
        num_msgs = len(self.data_model)
        for i in range(rows-1):
            index = num_msgs - i - 1
            if index < 0:
                continue
            self.stdscr.addstr(max(0, min(num_msgs, rows) - i - 2), 0, self.data_model[index])
        self.stdscr.move(rows-1, 0)
        self.stdscr.refresh()
