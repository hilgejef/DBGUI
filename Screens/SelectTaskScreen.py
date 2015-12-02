###############################################################################
# Author:		    Jonathon Moore
# Date Created:		12/01/2015
# Date Modified:	12/02/2015
# File Name:		SelectTaskScreen.py
#
# Overview:         Gives options to User for screen to access
#
#
###############################################################################

import sys
import curses
from CDBCore import CDBCore

class SelectTask(BaseScreen):
    def __init__(self, query=None, data=None):
        BaseScreen.__init__(self)

        #Action Widgets[]:      0 - TextBox for entering query string
        #                       1 - Button to submit Text query
        #                       2 - DataTable for displaying results
        self.ActionWidgets.append(Button(
            "1. View Tables",
            self.GoToViewTable,
            CDBCore.MAIN_SCREEN_Y + 5,
            30,
            None,
            True
        )
        self.ActionWidgets.append(Button(
            "2. Alter Existing Tables",
            self.GoToAlterTable,
            CDBCore.MAIN_SCREEN_Y + 6,
            30,
            None,
            True
        )
        self.ActionWidgets.append(Button(
            "3. Create a Table in Existing Database",
            self.GoToCreateTable,
            CDBCore.MAIN_SCREEN_Y + 7,
            30,
            None,
            True
        )
        self.ActionWidgets.append(Button(
            "4. Query Database",
            self.GoToQueryDatabase,
            CDBCore.MAIN_SCREEN_Y + 8,
            30,
            None,
            True
        )
        self.ActionWidgets.append(Button(
            "5. Edit Table Data",
            self.GoToEditTableResults,
            CDBCore.MAIN_SCREEN_Y + 9,
            30,
            None,
            True
        )
        self.ActionWidgets.append(Button(
            "6. Connect to a New Database",
            self.GoToConnectToNewDatabase,
            CDBCore.MAIN_SCREEN_Y + 10,
            30,
            None,
            True
        )
        self.ActionWidgets.append(Button(
            "7. Create a New Database",
            self.GoToCreateNewDatabase,
            CDBCore.MAIN_SCREEN_Y + 7,
            30,
            None,
            True
        )
        
        #Passive Widgets[]:     0 - Label to Select Screen
        self.PassiveWidgets.append(Label("Navigate to a Task:", CDBCore.MAIN_SCREEN_Y + 2, 30))
        
        self.Show()
        
    def GoToViewTable(self):
        pass
            
    def GoToAlterTable(self):
        pass
        
    def GoToCreateTable(self):
        pass
        
    def GoToQueryDatabase(self):
        pass
        
    def GoToEditTableResults(self):
        pass
        
    def GoToConnectToNewDatabase(self):
        pass
        
    def GoToCreateNewDatabase(self):
        pass

if __name__ == "__main__":
    user = raw_input('Enter the MySQL db user: ')
    password = raw_input('Enter the MySQL db user password: ')
    my = MySQLConnection(user, password)    
    my.Connect()
    CDBCore.InitCurses()
    CDBCore.InitScreens()
    #CDBCore.InitColor()
    CDBCore.ChangeCurrentScreen(SelectTask())
    CDBCore.Connection = my
    CDBCore.Main()