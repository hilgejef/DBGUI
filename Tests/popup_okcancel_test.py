import curses
from Core import Core
from Label import Label
from Button import Button
from BaseScreen import BaseScreen
from PopUp import PopUpOkCancel
from PopUp import PopUpYesNoCancel

def testMethod():
    pass
    
if __name__ == "__main__":
    Core.InitCurses()
    popup = PopUpOkCancel("This is a test", testMethod, testMethod)
    Core.CurrentScreen = popup
    Core.Main()