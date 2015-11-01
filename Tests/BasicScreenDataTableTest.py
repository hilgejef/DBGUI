import sys
import curses
from CDBCore import CDBCore
from Label import Label
from TextBox import TextBox
from Button import Button
from BaseScreen import BaseScreen
from DataTable import DataTable

class TestScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
    
    def Init(self):
        # Passive widgets
        lbl = Label("User Name:", 3, 3)
        lbltwo = Label("Password:", 6, 3)
        self.PassiveWidgets.append(lbl)
        self.PassiveWidgets.append(lbltwo)
        
        # Active widgets
        txtbox = TextBox(1, 16, 3, 20)
        txtboxtwo = TextBox(1, 16, 6, 20)
        datatable = DataTable(5, 16, 9, 20)
        btn = Button("EXIT", sys.exit, 15, 12)
        self.ActionWidgets.append(txtbox)
        self.ActionWidgets.append(txtboxtwo)
        self.ActionWidgets.append(datatable)
        self.ActionWidgets.append(btn)
    
if __name__ == "__main__":
    CDBCore.InitCurses()
    CDBCore.CurrentScreen = TestScreen()
    CDBCore.Main()