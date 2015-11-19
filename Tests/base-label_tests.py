import curses
from BaseWidget import BaseWidget
from Label import BaseLabel

# These actions will be handled in the Global file
stdscr = curses.initscr()
curses.start_color()
# Create color pairings
curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)

# Initialize main background color
stdscr.bkgd(' ', curses.color_pair(3))
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

# Testing BaseWidget
# bw = BaseWidget(1, 2, 3, 4)
# bw.Refresh()
# bw.Hide()
# bw.Show()
# bw.BordersOn()
# bw.BordersOff()
# bw.Move(6, 6)
# bw.ToTop()
# bw.ToBottom()

# Testing Label
stdscr.bkgd(' ', curses.color_pair(3))
stdscr.border()
lbl = BaseLabel("Hello", 5, 20, 3, 3, {"boxed":True})
lbltwo = BaseLabel("A second label!\nTEST", 5, 20, 10, 5, {"boxed":True})

# lbl.BordersOn()
# lbltwo.BordersOn()

# Pause to view
stdscr.getch()

# Clean up handled in Global file 
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()