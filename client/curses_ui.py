import os
import curses

class CursesUI:
    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)
        curses.noecho()
        curses.cbreak()

    def refresh(self):
        # Main loop
        #while 1:
            #c = stdscr.getch()
            #if c < 256:
                #stdscr.addstr(chr(c))
            #if c == ord('q'): break
        # show 5 most recent messages
        stdscr.refresh()

    def end_curses(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def set_message_list(self, list):
        self.msg_list = list
