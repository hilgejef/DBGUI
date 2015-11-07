import curses
from BaseWidget import BaseWidget
from Label import BaseLabel

# These actions will be handled in the Global file
stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

# Testing BaseWidget
bw = BaseWidget(1, 2, 3, 4)
bw.Refresh()
bw.Hide()
bw.Show()
bw.BordersOn()
bw.BordersOff()
bw.Move(6, 6)
bw.ToTop()
bw.ToBottom()

# Testing Label
lbl = BaseLabel("Hello", 2, 20, 3, 3)
lbltwo = BaseLabel("A second label!", 2, 20, 10, 5)

# Pause to view
stdscr.getch()

# Clean up handled in Global file 
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()