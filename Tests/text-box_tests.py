import curses
from BaseWidget import BaseWidget
from Label import Label
from TextBox import TextBox

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

# Testing TextBox
txtbox = TextBox(1, 16, 5, 15)
txtbox.CaptureText()

# Clean up handled in Global file 
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()

print txtbox.Value()