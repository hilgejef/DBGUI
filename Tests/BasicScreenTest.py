import sys
import curses
from CDBCore import CDBCore
from Label import Label
from BaseScreen import BaseScreen

class TestScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
    
#     def Init(self):
#         # Passive widgets
#         lbl = Label("User Name:", 3, 3)
#         lbltwo = Label("Password:", 6, 3)
#         self.PassiveWidgets.append(lbl)
#         self.PassiveWidgets.append(lbltwo)
    
if __name__ == "__main__":
    core = CDBCore()
    core.InitCurses()
    core.InitColor()
    core.CurrentScreen = TestScreen()
    core.Main()
