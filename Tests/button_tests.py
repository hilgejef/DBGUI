import curses
from BaseWidget import BaseWidget
from Label import Label
from TextBox import TextBox
from CheckBox import CheckBox
from Button import BaseButton


# These actions will be handled in the Global file
stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
stdscr.bkgd(' ', curses.color_pair(3))
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

def testMethod():
	pass

# Testing Button
btn = BaseButton("t", testMethod, 5, 20, 15, 15)
# btn.Active()
print btn.Text

# Clean up handled in Global file 
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()