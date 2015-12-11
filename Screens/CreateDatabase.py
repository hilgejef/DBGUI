###############################################################################
# CreateDatabase
#
# Overview:
#	Allows the user to create a new database. Only supported under
#	MySQL databases.
#
###############################################################################

import sys
import curses
import CDBCore
from Label import Label
from Button import Button
from TextBox import TextBox
from BaseScreen import BaseScreen
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
import SelectTaskScreen

class CreateDatabase(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)

    def Init(self):
        # Initialize this screens passive and action widgets
        self.PassiveWidgets.append(Label("Database Name:", CDBCore.CDBCore.MAIN_SCREEN_Y + 3, 3))
        self.ActionWidgets.append(TextBox(1, 16, CDBCore.CDBCore.MAIN_SCREEN_Y + 3, 25))
        self.ActionWidgets.append(Button("Create", self.Create, CDBCore.CDBCore.STATUS_SCREEN_Y - 3, 63))

    # Attempt to create the database
    def Create(self):
        try:
            name = self.ActionWidgets[0].Text
            result = CDBCore.CDBCore.Connection.QueryString("CREATE DATABASE " + name)
            if result.Success:
                CDBCore.CDBCore.StatusScreen.AddStatusMessage("Successfully created database: "+ name)
                curses.ungetch('\n') # Notify the core to move to next screen
            else:
                raise Exception(result.Message)
        except Exception as ex:
            msg = "Could not create database: " + name
            CDBCore.CDBCore.StatusScreen.AddStatusMessage(msg)
        
    # Go back to the selection screen
    def Next(self):
        return SelectTaskScreen.SelectTaskScreen()
        
if __name__ == "__main__":
    user = raw_input('Enter the MySQL db user: ')
    password = raw_input('Enter the MySQL db user password: ')
    my = MySQLConnection(user, password)    
    my.Connect()
    CDBCore.CDBCore.InitCurses(True)
    CDBCore.CDBCore.InitColor()
    CDBCore.CDBCore.InitScreens()
    CDBCore.CDBCore.CurrentScreen.Hide()
    CDBCore.CDBCore.CurrentScreen = CreateDatabase()
    CDBCore.CDBCore.Connection = my
    CDBCore.CDBCore.Main()