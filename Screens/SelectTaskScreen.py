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
from ViewDatabases import ViewDatabases
#from EditField import EditField
from CreateTable import CreateTable
from QueryTable import QueryTable
from CreateDatabase import CreateDatabase
from ConnectionWizard import ConnectionWizard

class SelectTask(BaseScreen):
    def __init__(self, query=None, data=None):
        BaseScreen.__init__(self)
        
    def Init(self):
        #Action Widgets[]:      0 - TextBox for entering query string
        #                       1 - Button to submit Text query
        #                       2 - DataTable for displaying results
        self.ActionWidgets.append(Button(
            ">> Use a New Connection",
            self.GoToNewConnection,
            CDBCore.MAIN_SCREEN_Y + 5,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button(
            ">> Choose a Database",
            self.GoToViewDatabases,
            CDBCore.MAIN_SCREEN_Y + 6,
            20,
            None,
            True
        ))
        #self.ActionWidgets.append(Button(
        #    "1. View Table",
        #    self.GoToViewTable,
        #    CDBCore.MAIN_SCREEN_Y + 5,
        #    20,
        #    None,
        #    True
        #))
        #self.ActionWidgets.append(Button(
        #    "2. Alter Existing Tables",
        #    self.GoToAlterTable,
        #    CDBCore.MAIN_SCREEN_Y + 6,
        #    20,
        #    None,
        #    True
        #))
        self.ActionWidgets.append(Button(
            ">> Create a New Table",
            self.GoToCreateTable,
            CDBCore.MAIN_SCREEN_Y + 7,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button(
            ">> Create a New Database",
            self.GoToCreateNewDatabase,
            CDBCore.MAIN_SCREEN_Y + 8,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button(
            ">> Query Database",
            self.GoToQueryDatabase,
            CDBCore.MAIN_SCREEN_Y + 9,
            20,
            None,
            True
        ))
        self.ActionWidgets.append(Button(
            ">> Edit Table Data",
            self.GoToEditTableResults,
            CDBCore.MAIN_SCREEN_Y + 10,
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
        
    def GoToNewConnection(self):
        CDBCore.History.append(CDBCore.CurrentScreen)
        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = ConnectionWizard()
        #nextscreen = ConnectionWizard()
        #CDBCore.ChangeCurrentScreen(nextscreen)
        
    def GoToViewDatabases(self):
        CDBCore.History.append(CDBCore.CurrentScreen)
        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = ViewDatabases()
        #nextscreen = ViewDatabases()
        #CDBCore.ChangeCurrentScreen(nextscreen)
        
    def GoToViewTable(self):
        CDBCore.History.append(CDBCore.CurrentScreen)
        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = ViewTable()
        #nextscreen = ViewTables()
        #CDBCore.ChangeCurrentScreen(nextscreen)
            
    def GoToAlterTable(self):
        #TODO: Connect when screen is done
        pass
        #nextscreen = EditField()
        #CDBCore.ChangeCurrentScreen(nextscreen)
        
    def GoToCreateTable(self):
        CDBCore.History.append(CDBCore.CurrentScreen)
        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = CreateTable()
        #nextscreen = CreateTable()
        #CDBCore.ChangeCurrentScreen(nextscreen)
        
    def GoToQueryDatabase(self):
        CDBCore.History.append(CDBCore.CurrentScreen)
        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = CreateTable()
        #nextscreen = QueryTable()
        #CDBCore.ChangeCurrentScreen(nextscreen)
        
    def GoToEditTableResults(self):
        #TODO - screen not yet made
        pass
        
    def GoToCreateNewDatabase(self):
        CDBCore.History.append(CDBCore.CurrentScreen)
        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = CreateTable()
        #nextscreen = CreateDatabase()
        #CDBCore.ChangeCurrentScreen(nextscreen)
        
    def GoToCoreShutdown(self):
        pass
        #TODO: how do we exit the program?

if __name__ == "__main__":
    CDBCore.InitCurses()
    CDBCore.InitScreens()
    #CDBCore.InitColor()
    CDBCore.History.append(CDBCore.CurrentScreen)
    CDBCore.CurrentScreen.Hide()
    CDBCore.CurrentScreen = SelectTask()
    CDBCore.Main()