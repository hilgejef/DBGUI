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

class CreateDatabase(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)

    def Init(self):
        self.PassiveWidgets.append(Label("Database Name:", 5, 5))
        self.ActionWidgets.append(TextBox(1, 16, 5, 20))
        #TODO: Replace with back button?
        self.ActionWidgets.append(Button("Exit", sys.exit, 23, 5))
        self.ActionWidgets.append(Button("Create", self.Create, 23, 15))

    def Create(self):
        try:
            name = self.ActionWidgets[0].Text
            result = CDBCore.Connection.QueryString("CREATE DATABASE " + name)
            if result.Success:
                #TODO: Add status update here that database was created successfully
                curses.ungetch('\n') # Notify the core to move to next screen
            else:
                raise Exception(result.Message)
        except Exception as ex:
            # TODO: Add status update here, and keep the screen here
            msg = "Could not retrieve list of databases.\n" + str(ex)
        
        
    # TODO: Return the next screen
    def Next(self):
        return None
        
if __name__ == "__main__":
    user = raw_input('Enter the MySQL db user: ')
    password = raw_input('Enter the MySQL db user password: ')
    my = MySQLConnection(user, password)    
    my.Connect()
    CDBCore.InitCurses()
    CDBCore.CurrentScreen = CreateDatabase()
    CDBCore.Connection = my
    CDBCore.Main()