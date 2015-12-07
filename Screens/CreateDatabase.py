###############################################################################
# Author:		Rich Gagliano
# Date Created:		11/16/2015
# Date Modified:	11/19/2015
# File Name:		CreateDatabase.py
#
# Overview:
#
#
###############################################################################

import sys
import curses
from CDBCore import CDBCore
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
        self.PassiveWidgets.append(Label("Database Name:", CDBCore.MAIN_SCREEN_Y + 3, 3))
        self.ActionWidgets.append(TextBox(1, 16, CDBCore.MAIN_SCREEN_Y + 3, 25))
        self.ActionWidgets.append(Button("Create", self.Create, CDBCore.STATUS_SCREEN_Y - 3, 63))

    def Create(self):
        try:
            name = self.ActionWidgets[0].Text
            result = CDBCore.Connection.QueryString("CREATE DATABASE " + name)
            if result.Success:
                CDBCore.StatusScreen.AddStatusMessage("Successfully created database: "+ name)
                curses.ungetch('\n') # Notify the core to move to next screen
            else:
                raise Exception(result.Message)
        except Exception as ex:
            # TODO: Replace with error once multi line is supported
            msg = "Could not create database: " + name
            CDBCore.StatusScreen.AddStatusMessage(msg)
        
    # Go back to the selection screen
    def Next(self):
        return SelectTaskScreen.SelectTaskScreen()
        
if __name__ == "__main__":
    user = raw_input('Enter the MySQL db user: ')
    password = raw_input('Enter the MySQL db user password: ')
    my = MySQLConnection(user, password)    
    my.Connect()
    CDBCore.InitCurses(True)
    CDBCore.InitColor()
    CDBCore.InitScreens()
    CDBCore.CurrentScreen.Hide()
    CDBCore.CurrentScreen = CreateDatabase()
    CDBCore.Connection = my
    CDBCore.Main()