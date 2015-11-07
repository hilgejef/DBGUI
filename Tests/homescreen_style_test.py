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
        button = BaseButton("OK", 5, 5, 11, 11)

if __name__ == "__main__":
    CDBCore.InitCurses()
    CDBCore.CurrentScreen = HomeScreen()
    CDBCore.Main()