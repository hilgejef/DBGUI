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
    CDBCore.InitCurses()
    popup = PopUpYesNoCancel("This is a test", testMethod, testMethod, testMethod)
    CDBCore.CurrentScreen = popup
    CDBCore.Main()