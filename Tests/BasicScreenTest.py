import sys
import curses
from CDBCore import CDBCore
from Label import Label
from TextBox import TextBox
from Button import Button
from BaseScreen import BaseScreen

class TestScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
    
    def Init(self):
        # Passive widgets
        lbl = Label("User Name:", 3, 3)
        lbltwo = Label("Password:", 6, 3)
        self.PassiveWidgets.append(lbl)
        self.PassiveWidgets.append(lbltwo)
    
if __name__ == "__main__":
    CDBCore.InitCurses()
    CDBCore.InitColor()
    CDBCore.CurrentScreen = TestScreen()
    CDBCore.Main()