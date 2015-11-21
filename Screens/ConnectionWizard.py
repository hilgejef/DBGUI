###############################################################################
# Author:		Rich Gagliano
# Date Created:		11/9/2015
# Date Modified:	11/10/2015
# File Name:		ConnectionWizard.py
#
# Overview:
#
#
###############################################################################

import sys
import curses
from CDBCore import CDBCore
from Label import Label
from TextBox import TextBox
from Button import Button
from BaseScreen import BaseScreen
from CheckBox import CheckBox
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection

class ConnectionWizard(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
    
    def Init(self):
        # Tracking variables for retrieving entries
        self.Items = ["User Name", "Password", "Host", "Port", "Database (Optional)", "MySQL", "PostgreSQL"]        
        self.Input = {}
        for i in range(len(self.Items)):
            self.Input[self.Items[i]] = i
        
        # Spacing
        yoffset = 0
        ystart = 3
        xlabel = 3
        xaction = 25
        
        # Passive widgets
        for i in range(len(self.Items)):
            y = (ystart * (i + 1)) + yoffset
            self.PassiveWidgets.append(Label(self.Items[i], y, xlabel))
        
        # Active widgets
        self.ActionWidgets.append(TextBox(1, 16, 3 + yoffset, xaction))
        self.ActionWidgets.append(TextBox(1, 16, 6 + yoffset, xaction))
        self.ActionWidgets.append(TextBox(1, 16, 9 + yoffset, xaction))
        self.ActionWidgets.append(TextBox(1, 16, 12 + yoffset, xaction))
        self.ActionWidgets.append(TextBox(1, 16, 15 + yoffset, xaction))
        self.ActionWidgets.append(CheckBox('X', ' ', 18 + yoffset, xaction))
        self.ActionWidgets.append(CheckBox('X', ' ', 21 + yoffset, xaction))
        self.ActionWidgets.append(Button("Exit", sys.exit, 23 + yoffset, 5))
        self.ActionWidgets.append(Button("Next", self.TestConnection, 23 + yoffset, 12))
    
    # Test the user entered information to ensure a connection
    # can be established
    def TestConnection(self):
        database = None
        if len(self.ActionWidgets[self.Input["Database (Optional)"]].Text) > 0:
            database = self.ActionWidgets[self.Input["Database (Optional)"]].Text
        con = MySQLConnection(self.ActionWidgets[self.Input["User Name"]].Text,
                              self.ActionWidgets[self.Input["Password"]].Text,
                              self.ActionWidgets[self.Input["Host"]].Text,
                              int(self.ActionWidgets[self.Input["Port"]].Text))
        results = con.Connect()
        if results.Success:
            CDBCore.Connection = con
            curses.ungetch('\n') # Notify the core to move to next screen
        else:
            # TODO: Status and popup here with failure message
            self.ActionWidgets[0].selected = True
            self.ActionWidgets[0].Highlight()
            self.ActionWidgets[0].Active
    
    # TODO: Return the next screen
    def Next(self):
        return None
        
if __name__ == "__main__":
    CDBCore.InitCurses()
    CDBCore.CurrentScreen = ConnectionWizard()
    CDBCore.Main()