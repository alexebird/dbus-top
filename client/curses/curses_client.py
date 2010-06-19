#!/usr/bin/python

import signal, os
import curses

# Init curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

# Main loop
while 1:
    c = stdscr.getch()
    if c < 256:
        stdscr.addstr(chr(c))
    if c == ord('q'): break
    stdscr.refresh()

# End curses
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()

class CursesClient(DBusClient):
    def __init__(self):
        pass
