import sys
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
    CDBCore.InitCurses(debug=True)
    CDBCore.InitColor()
    popup = PopUpYesNoCancel("This is a test", testMethod, testMethod, sys.exit)
    CDBCore.CurrentScreen = popup
    CDBCore.Main()