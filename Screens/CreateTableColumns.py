###############################################################################
# Author:		Rich Gagliano
# Date Created:		11/21/2015
# Date Modified:	11/23/2015
# File Name:		CreateTableColumns.py
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
from BaseScreen import BaseScreen
from CheckBox import CheckBox
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection

class CreateTableColumns(BaseScreen):
    def __init__(self, name, columns):
        self.Name = name
        self.Columns = columns
        BaseScreen.__init__(self)
        
    def Init(self):
        # Spacing
        yoffset = 0
        ystart = 3
        xlabel = 3
        xaction = 15
      
        # Tracking variables for retrieving entries
        self.Fields = ["ColumnName", "ColumnType"]
        self.Indexes = {}
        counter = 0
        for c in range(self.Columns):
            self.PassiveWidgets.append(Label("Field" + str(c), ystart + yoffset, xlabel))
            for f in self.Fields:
                self.Indexes[f + str(c)] = counter
                self.ActionWidgets.append(TextBox(1, 16, ystart + yoffset, xaction))
                counter += 1
                xaction = 35
            yoffset += 3
            xaction = 15        
        
        self.PassiveWidgets.append(Label("Column Name", 0, 15))
        self.PassiveWidgets.append(Label("Column Type", 0, 35))
        self.ActionWidgets.append(Button("Exit", sys.exit, ystart + yoffset, 5))
        self.ActionWidgets.append(Button("Create", self.CreateTable, ystart + yoffset, 15))

    def ConstructQuery(self):
        header = "CREATE TABLE " + self.Name + "("
        body = ""
        
        indexes = (self.Columns * 2) - 1
        counter = 0
        while counter < indexes:
            body += self.ActionWidgets[counter].Text
            counter += 1
            body = body + " " + self.ActionWidgets[counter].Text
            counter += 1
            if counter < indexes:
                body += ", "
        
        footer = ")"
        return header + body + footer
        
    def CreateTable(self):
        try:
            # Construct the create table query from the user's input
            query = self.ConstructQuery()
            
            # Attempt to create the table
            result = CDBCore.Connection.QueryString(query)
            
            # Ensure that the query was successful
            if not result.Success:
                raise Exception(result.Message)
            
            # Move on to next screen
            curses.ungetch('\n')
            
        except Exception as ex:
            # TODO: Add status update here, and keep the screen here
            msg = "Failed to create table:\n" + str(ex)
            self.Columns = 0
            self.Name = ""
            self.ActionWidgets[0].selected = True
            self.ActionWidgets[0].Highlight()
            self.ActionWidgets[0].Active()
            return
        
    # Move on to CreateTableColumn
    def Next(self):
        return None
        
if __name__ == "__main__":
    user = raw_input('Enter the MySQL db user: ')
    password = raw_input('Enter the MySQL db user password: ')
    host = raw_input('Enter the MySQL db host: ')
    port = raw_input('Enter the MySQL db port: ')
    database = raw_input('Enter the MySQL db database: ')
    name = raw_input('Enter the name of your new table: ')
    columns = raw_input('How many columns would you like? (1-10): ')
    my = MySQLConnection(user, password, host, int(port), database)    
    result = my.Connect()
    if result.Success:
        CDBCore.InitCurses()
        CDBCore.CurrentScreen = CreateTableColumns(name, int(columns))
        CDBCore.Connection = my
        CDBCore.Main()    
    else:
        print "Could not log in: " + result.Message        