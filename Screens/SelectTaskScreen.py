###############################################################################
# SelectTaskScreen
#
# Overview:         
#	Gives options to User for screen to access
#
#
###############################################################################

import sys
import curses
import MySQLConnection
import CDBCore
import BaseScreen
import Button
import Label
import ViewTables
import ViewDatabases
from CreateTable import CreateTable
from QueryTable import QueryTable
from QueryDatabase import QueryDatabase
from CreateDatabase import CreateDatabase
from ConnectionWizard import ConnectionWizard
from PopUp import PopUpOk

class SelectTaskScreen(BaseScreen.BaseScreen):
    def __init__(self, query=None, data=None):
        BaseScreen.BaseScreen.__init__(self, screen_type="SelectTask")
        
    def Init(self):
        # next screen
        self.NextScreen = None
        self.Screens = [
            ConnectionWizard,
            ViewDatabases.ViewDatabases,
            CreateTable,
            ViewTables.ViewTables,
            CreateDatabase,
            QueryDatabase
        ]
        
        #Action Widgets[]:      0..X:  select window screen
        self.ActionWidgets.append(Button.Button(
            ">> Use a New Connection",
            self.SetNextScreen,
            CDBCore.CDBCore.MAIN_SCREEN_Y + 5,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button.Button(
            ">> Choose a Database",
            self.SetNextScreen,
            CDBCore.CDBCore.MAIN_SCREEN_Y + 6,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button.Button(
            ">> Create a New Table",
            self.SetNextScreen,
            CDBCore.CDBCore.MAIN_SCREEN_Y + 7,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button.Button(
            ">> View Tables",
            self.SetNextScreen,
            CDBCore.CDBCore.MAIN_SCREEN_Y + 8,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button.Button(
            ">> Create a New Database",
            self.SetNextScreen,
            CDBCore.CDBCore.MAIN_SCREEN_Y + 9,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button.Button(
            ">> Query Database",
            self.SetNextScreen,
            CDBCore.CDBCore.MAIN_SCREEN_Y + 10,
            20,
            None,
            True
        ))
        
        
        # EXIT BUTTON GOES LAST
        self.ActionWidgets.append(Button.Button(
            "Exit Program",
            self.GoToCoreShutdown,
            CDBCore.CDBCore.MAIN_SCREEN_Y + 12,
            20,
            None,
            True
        ))
        
        #Passive Widgets[]:     0 - Label to Select Screen
        self.PassiveWidgets.append(Label.Label("Select a Task:", CDBCore.CDBCore.MAIN_SCREEN_Y + 2, 30))
        CDBCore.CDBCore.StatusScreen.AddStatusMessage("Use Tab to change and Enter to select")
        
        self.Show()
        
    def SetNextScreen(self):
        # if connection is set or user is going to ConnectionWizard screen
        if not CDBCore.CDBCore.Connection and self.CurrentWidget > 0:
            msg = "Error: No Connection Detected.\nSelect Connection Wizard to connect to a\ndatabase."
            CDBCore.CDBCore.StatusScreen.AddStatusMessage(msg)
            CDBCore.CDBCore.PopUp = PopUpOk(msg)
            CDBCore.CDBCore.PopUp.MakeActive()
        # if a connection is established but a database is not set
        elif CDBCore.CDBCore.Connection and not CDBCore.CDBCore.Connection.Database and (self.CurrentWidget == 4 or self.CurrentWidget == 5):
            msg = "Error: No Database Detected.\nSelect or Create a Database first."
            CDBCore.CDBCore.StatusScreen.AddStatusMessage(msg)
            CDBCore.CDBCore.PopUp = PopUpOk(msg)
            CDBCore.CDBCore.PopUp.MakeActive()
        elif CDBCore.CDBCore.Connection and CDBCore.CDBCore.Connection.DBType == "PostgreSQL" and self.CurrentWidget == 4:
            msg = "Error: Cannot create databases when using\nPostgreSQL connector.\n\nUse PSQL tool."
            CDBCore.CDBCore.StatusScreen.AddStatusMessage(msg)
            CDBCore.CDBCore.PopUp = PopUpOk(msg)
            CDBCore.CDBCore.PopUp.MakeActive()
        else:
            self.NextScreen = self.Screens[self.CurrentWidget]
            curses.ungetch('\n')
            
            
        
    # overwriting virtual method indicating where the next screen should go
    def Next(self):
        return self.NextScreen()
        
    def GoToCoreShutdown(self):
        sys.exit(0)

# Test the screen separately
if __name__ == "__main__":
    user = raw_input('Enter the MySQL db user: ')
    password = raw_input('Enter the MySQL db user password: ')
    my = MySQLConnection.MySQLConnection(user, password)    
    my.Connect()
    CDBCore.CDBCore.InitCurses()
    CDBCore.CDBCore.InitScreens()
    CDBCore.InitColor()
    CDBCore.CDBCore.History.append(CDBCore.CurrentScreen)
    CDBCore.CDBCore.CurrentScreen.Hide()
    CDBCore.CDBCore.CurrentScreen = SelectTaskScreen()
    CDBCore.CDBCore.Connection = my
    CDBCore.CDBCore.Main()