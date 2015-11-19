import curses

stdscr = curses.initscr()
key = stdscr.getch()
print key