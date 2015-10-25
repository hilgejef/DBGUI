import curses
from BaseWidget import BaseWidget
from Label import Label
from PopUp import PopUp

# These actions will be handled in the Global file
stdscr = curses.initscr()
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
lbl = Label("Hello", 3, 3)
lbltwo = Label("A second label!", 10, 5)

# Testing Popup
popup = PopUp("Alert! Something something!", 1, 1)
popup.Active()

stdscr.getch()

# Clean up handled in Global file 
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()

