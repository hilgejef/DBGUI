import curses
from BaseWidget import BaseWidget
from DataTable import DataTable

# These actions will be handled in the Global file
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

# Test DataTable
datatbl = DataTable(8, 30, 2, 2)
datatbl.Active()

# Clean up handled in Global file 
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()