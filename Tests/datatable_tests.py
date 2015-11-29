import curses
from BaseWidget import BaseWidget
from Label import Label
from TextBox import TextBox
from DataTable import DataTable

# These actions will be handled in the Global file
stdscr = curses.initscr()
curses.start_color()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

# label testing
lbl = Label("TestLabel", 2, 2)
txtbx = TextBox(5, 30, 2, 20)

# Test DataTable
resultsobj = [["colA", "columnB", "CCCCCCCCCCCCCCCCC", "colD"],
             [["data00", "data01", "data02", "data03"],
              ["datahereis toolong", "more data here", "row2data3", "data13"],
              ["20", "21", "22", "23"],
              ["aa", "ab", "ac", "ad"],
              ["once upon a time there was ", "test test test", "datadatadata", "allofthis is f"],
              ["", "", "", ""],
              ["last0", "last1", "last2", "last3"],
              ]]
datatbl = DataTable(8, 30, 10, 4, resultsobj)
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