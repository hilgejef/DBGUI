import curses
from BaseWidget import BaseWidget
from DataTable import DataTable

# These actions will be handled in the Global file
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

# Test DataTable
datatbl = DataTable(8, 30, 10, 4)
datatbl.Active()

# Clean up handled in Global file 
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()



#print "Y=" + str(datatbl.Y)
#print "X=" + str(datatbl.X)
#print "Rows=" + str(datatbl.Rows)
#print "Columns=" + str(datatbl.Columns)
#print "RowHeight=" + str(datatbl.RowHeight)
#print "ColWidth=" + str(datatbl.ColWidth)
#print "TotalY=" + str(datatbl.TotalY)
#print "TotalX=" + str(datatbl.TotalX)