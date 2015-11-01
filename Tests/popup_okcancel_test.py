import curses
from CDBCore import CDBCore
from Label import Label
from Button import Button
from BaseScreen import BaseScreen
from PopUp import PopUpOkCancel
from PopUp import PopUpYesNoCancel

def testMethod():
    pass
    
if __name__ == "__main__":
    stdscr = curses.initscr()
    popup = PopUpOkCancel("This is a test", testMethod, testMethod)
    print len(popup.ActiveWidgets)
    print popup.CurrentWidget