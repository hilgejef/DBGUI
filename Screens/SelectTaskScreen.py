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
from MySQLConnection import MySQLConnection
from CDBCore import CDBCore
from BaseScreen import BaseScreen
from Button import Button
from Label import Label
from ViewTables import ViewTables
import ViewDatabases
#from EditField import EditField
from CreateTable import CreateTable
from QueryTable import QueryTable
from QueryDatabase import QueryDatabase
from CreateDatabase import CreateDatabase
from ConnectionWizard import ConnectionWizard
from PopUp import PopUpOk

class SelectTask(BaseScreen):
    def __init__(self, query=None, data=None):
        BaseScreen.__init__(self)
        
    def Init(self):
        # next screen
        self.NextScreen = None
        self.Screens = [
            ConnectionWizard,
            ViewDatabases.ViewDatabases,
            CreateTable,
            CreateDatabase,
            QueryDatabase
        ]
        
        #Action Widgets[]:      0..X:  select window screen
        self.ActionWidgets.append(Button(
            ">> Use a New Connection",
            self.SetNextScreen,
            CDBCore.MAIN_SCREEN_Y + 5,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button(
            ">> Choose a Database",
            self.SetNextScreen,
            CDBCore.MAIN_SCREEN_Y + 6,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button(
            ">> Create a New Table",
            self.SetNextScreen,
            CDBCore.MAIN_SCREEN_Y + 7,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button(
            ">> Create a New Database",
            self.SetNextScreen,
            CDBCore.MAIN_SCREEN_Y + 8,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button(
            ">> Query Database",
            self.SetNextScreen,
            CDBCore.MAIN_SCREEN_Y + 9,
            20,
            None,
            True
        ))
        
        # EXIT BUTTON GOES LAST
        self.ActionWidgets.append(Button(
            "Exit Program",
            self.GoToCoreShutdown,
            CDBCore.MAIN_SCREEN_Y + 12,
            20,
            None,
            True
        ))
        
        #Passive Widgets[]:     0 - Label to Select Screen
        self.PassiveWidgets.append(Label("Select a Task:", CDBCore.MAIN_SCREEN_Y + 2, 30))
        CDBCore.StatusScreen.AddStatusMessage("Use Tab to change and Enter to select")
        
        self.Show()
        
    def SetNextScreen(self):
        # if connection is set or user is going to ConnectionWizard screen
        if not CDBCore.Connection and self.CurrentWidget > 0:
            msg = "Error: No Connection Detected.\nSelect Connection Wizard to connect to a\ndatabase."
            CDBCore.StatusScreen.AddStatusMessage(msg)
            CDBCore.PopUp = PopUpOk(msg)
            CDBCore.PopUp.MakeActive()
        # if a connection is established but a database is not set
        elif not CDBCore.Connection.Database and self.CurrentWidget == 4:
            msg = "Error: No Database Detected.\nSelect or Create a Database first."
            CDBCore.StatusScreen.AddStatusMessage(msg)
            CDBCore.PopUp = PopUpOk(msg)
            CDBCore.PopUp.MakeActive()
        else:
            self.NextScreen = self.Screens[self.CurrentWidget]
            curses.ungetch('\n')
            
            
        
    # overwriting virtual method indicating where the next screen should go
    def Next(self):
        return self.NextScreen()
        
    def GoToCoreShutdown(self):
        sys.exit(0)

if __name__ == "__main__":
    user = raw_input('Enter the MySQL db user: ')
    password = raw_input('Enter the MySQL db user password: ')
    my = MySQLConnection(user, password)    
    my.Connect()
    CDBCore.InitCurses()
    CDBCore.InitScreens()
    #CDBCore.InitColor()
    CDBCore.History.append(CDBCore.CurrentScreen)
    CDBCore.CurrentScreen.Hide()
    CDBCore.CurrentScreen = SelectTask()
    CDBCore.Connection = my
    CDBCore.Main()