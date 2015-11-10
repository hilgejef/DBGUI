import curses
import curses.panel
from HomeScreen import HomeScreen
from CDBCore import CDBCore

if __name__ == "__main__":
    print "Initializing and Displaying HomeScreen" # TESTING
    CDBCore.InitCurses()
    CDBCore.InitColor()
    CDBCore.CurrentScreen = HomeScreen()
    CDBCore.Main()