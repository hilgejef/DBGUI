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

class ViewDatabases(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)

    def Init(self):
        self.GetDatabases()
        self.PassiveWidgets.append(Label("Databases", CDBCore.MAIN_SCREEN_Y + 3, 5))
        
    # Retrieves a list of databases
    def GetDatabases(self):
        try:
            # Retrieve a list of databses
            result = CDBCore.Connection.QueryString("SHOW DATABASES")
            
            # Ensure there weren't any issues getting the list of databases.
            if not result.Success:
                raise Exception(result.Message)
            
            # Create a button for each database
            offset = CDBCore.MAIN_SCREEN_Y + 5
            for name in result.Data[1]:
                self.ActionWidgets.append(Button(name[0], self.SetDatabase, offset, 5))
                offset += 2
        except Exception as ex:
            # TODO: Once multi line is supported, add in error message
            msg = "Could not retrieve list of databases."
            CDBCore.StatusScreen.AddStatusMessage(msg + str(ex))
            print str(ex)
            

    # Sets the current database
    def SetDatabase(self):
        try:
            name = self.ActionWidgets[self.CurrentWidget].Text
            name = name[2:] # Clean up the bracket '[ ' in the button text
            name = name[:-2] # Clean up the bracket ' ]' in the button text
            CDBCore.Connection.Database = name
            result = CDBCore.Connection.QueryString("USE " + name)
            if result.Success:
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

    # TODO: Return the next screen
    def Next(self):
        return None

if __name__ == "__main__":
    user = raw_input('Enter the MySQL db user: ')
    password = raw_input('Enter the MySQL db user password: ')
    my = MySQLConnection(user, password)    
    result = my.Connect()
    if result.Success:
        CDBCore.InitCurses(True)
        CDBCore.InitColor()
        CDBCore.InitScreens()
        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = ViewDatabases()
        CDBCore.Connection = MySQLConnection(user, password)
        CDBCore.Main()
    else:
        print "Could not log in: " + result.Message