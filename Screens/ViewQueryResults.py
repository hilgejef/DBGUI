###############################################################################
# Author:		    Jonathon Moore
# Date Created:		11/17/2015
# Date Modified:	11/17/2015
# File Name:		ViewQueryResults.py
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
from DataTable import DataTable
from BaseScreen import BaseScreen
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection

class ViewQueryResults(BaseScreen):
    def __init__(self, query=None, data=None):
        BaseScreen.__init__(self)

        #Action Widgets[]:      0 - TextBox for entering query string
        #                       1 - Button to submit Text query
        #                       2 - DataTable for displaying results
        self.ActionWidgets.append(TextBox(3, 50, CDBCore.MAIN_SCREEN_Y + 1, 15))
        self.ActionWidgets.append(Button("Submit", self.ExecuteQuery, CDBCore.MAIN_SCREEN_Y + 1, 70))
        self.ActionWidgets.append(DataTable(12, 70, CDBCore.MAIN_SCREEN_Y + 6, 5, data))
        self.ActionWidgets[2].SetColumnWidth(16)
        
        #Passive Widgets[]:     0 - Label for Query String
        #                       1 - top border for textbox
        #                       2 - bottom border for textbox
        self.PassiveWidgets.append(Label("Enter Query:", CDBCore.MAIN_SCREEN_Y + 1, 2))
        if not (query is None):
            # if query is given then add that to textbox
            self.PassiveWidgets[0].Text = query
            self.PassiveWidgets[0].UpdateDisplay()
        self.PassiveWidgets.append(Label('-' * 50, CDBCore.MAIN_SCREEN_Y, 15))
        self.PassiveWidgets.append(Label('-' * 50, CDBCore.MAIN_SCREEN_Y + 4, 15))
        
        self.Show()
        
    def ExecuteQuery(self):
        pass
            

if __name__ == "__main__":
    user = raw_input('Enter the MySQL db user: ')
    password = raw_input('Enter the MySQL db user password: ')
    my = MySQLConnection(user, password)    
    my.Connect()
    CDBCore.InitCurses()
    CDBCore.InitColor()
    CDBCore.CurrentScreen = ViewQueryResults()
    CDBCore.Connection = my
    CDBCore.Main()