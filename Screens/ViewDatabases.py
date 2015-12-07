###############################################################################
# Author:		Rich Gagliano
# Date Created:		11/13/2015
# Date Modified:	11/15/2015
# File Name:		ViewDatabases.py
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
from BaseScreen import BaseScreen
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
from PostgresConnection import PostgresConnection
from DataTable import DataTable
from SelectTaskScreen import SelectTaskScreen

class ViewDatabases(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)

    def Init(self):
        self.dbs = self.GetDatabases()
    
    # Retrieves a list of databases
    def GetDatabases(self):
        try:
            # Retrieve a list of databses
            result = CDBCore.Connection.GetDatabases()
            
            # Ensure there weren't any issues getting the list of databases.
            if not result.Success:
                raise Exception(result.Message)
            
            # Create a button for each database
            self.ActionWidgets.append(DataTable(CDBCore.MAIN_SCREEN_LINES - 6, 70, CDBCore.MAIN_SCREEN_Y + 2, 3, result.Data, 50))
            self.ActionWidgets.append(Button("Connect", self.SetDatabase, CDBCore.STATUS_SCREEN_Y - 3, 25))
            
        except Exception as ex:
            # TODO: Once multi line is supported, add in error message
            msg = "Could not retrieve list of databases."
            CDBCore.StatusScreen.AddStatusMessage(msg + str(ex))
            print str(ex)
            

    # Sets the current database
    def SetDatabase(self):
        try:
            name = self.ActionWidgets[0].Text            
            result = CDBCore.Connection.SetDatabase(name)
            if result.Success:
                CDBCore.Connection.Database = name
                CDBCore.StatusScreen.AddStatusMessage("Set database to: " + name)
                curses.ungetch('\n') # Notify the core to move to next screen
            else:
                raise Exception(result.Message)
        except Exception as ex:
            # TODO: Once multi line is supported, add in error message
            msg = "Could not set the database to: " + name
            CDBCore.StatusScreen.AddStatusMessage(msg)
            self.ActionWidgets[self.CurrentWidget].selected = True
            self.ActionWidgets[self.CurrentWidget].Highlight()
            self.ActionWidgets[self.CurrentWidget].Active

    # Go back to the selection screen
    def Next(self):
        return SelectTaskScreen()

if __name__ == "__main__":
    db = raw_input('Database type (p for Postgres, m for MySQL: ')
    user = raw_input('Enter the db user: ')
    password = raw_input('Enter the db user password: ')   
    my = None
    if db == "m":
        my = MySQLConnection(user, password)
    else:
        my = PostgresConnection(user, password)    
    result = my.Connect()
    if result.Success:
        CDBCore.InitCurses(True)
        CDBCore.InitColor()
        CDBCore.InitScreens()
        CDBCore.Connection = my
        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = ViewDatabases()
        CDBCore.Main()
    else:
        print "Could not log in: " + result.Message