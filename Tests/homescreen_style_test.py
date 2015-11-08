import curses
import curses.panel
from BaseScreen import BaseScreen
from Label import BaseLabel
from Button import BaseButton
from CDBCore import CDBCore

def testMethod():
    pass

class HomeScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
        label = BaseLabel("Welcome to Database Explorer", 10, 10, 1, 1)
        BaseScreen.PassiveWidgets.append(label)

if __name__ == "__main__":
    print "Initializing and Displaying HomeScreen" # TESTING
    CDBCore.InitCurses()
    CDBCore.InitColor()
    CDBCore.CurrentScreen = HomeScreen()
    CDBCore.Main()