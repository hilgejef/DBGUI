import curses
import curses.panel
from MainMenu import MainMenu
from HomeScreen import HomeScreen
from CDBCore import CDBCore

if __name__ == "__main__":
    print "Initializing and Displaying HomeScreen" # TESTING
    CDBCore.InitCurses(debug=True)
    CDBCore.InitColor()
    CDBCore.MenuScreen = MainMenu()
    CDBCore.CurrentScreen = HomeScreen()
    CDBCore.Main()