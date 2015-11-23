###############################################################################
# Author:		Rich Gagliano
# Date Created:		11/21/2015
# Date Modified:	11/23/2015
# File Name:		CreateTable.py
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
from CreateTableColumns import CreateTableColumns

class CreateTable(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
        self.Name = ""
        self.Columns = 0
    
    def Init(self):
        self.PassiveWidgets.append(Label("Table Name:", 5, 5))
        self.PassiveWidgets.append(Label("Number of Columns:", 7, 5))
        self.ActionWidgets.append(TextBox(1, 16, 5, 20))
        self.ActionWidgets.append(TextBox(1, 16, 7, 20))
        self.ActionWidgets.append(Button("Exit", sys.exit, 10, 5))
        self.ActionWidgets.append(Button("Next", self.CheckValues, 10, 15))
    
    # Checks if a table already exists under the requested name
    def CheckName(self):
        try:
            # Retrieve listing of tables
            result = CDBCore.Connection.QueryString("SHOW TABLES")
            
            # Ensure that the query was successful
            if not result.Success:
                raise Exception(result.Message)
            
            # Check for the table name
            for existing_name in result.Data[1]:
                if existing_name == self.Name:
                    #TODO: Log to status screen
                    msg = "Table name " + str(self.Name) + " already exists."
                    return False
            
            # This is a new table name
            return True
        except Exception as ex:
            #TODO: write to status
            msg = "Could not retrieve list of tables.\n" + str(ex)
            return False
    
    def CheckValues(self):
        try:
            self.Name = self.ActionWidgets[0].Text
            self.Columns = int(self.ActionWidgets[1].Text)
            
            # For now impose limit on columns until pagination
            if self.Columns > 10 or self.Columns < 1:
                # TODO: Add status update here, and keep the screen here
                msg = "Arbitrary limitation of 1-10 columns not met!\n"
                self.Columns = 0
                self.Name = ""
                self.ActionWidgets[0].selected = True
                self.ActionWidgets[0].Highlight()
                self.ActionWidgets[0].Active()
                return
            
            # Check to see if the table name already exists
            if not self.CheckName():
                self.Columns = 0
                self.Name = ""
                self.ActionWidgets[0].selected = True
                self.ActionWidgets[0].Highlight()
                self.ActionWidgets[0].Active()
                return
            
            # Move on to CreateTableColumn
            curses.ungetch('\n')
            
        except Exception as ex:
            # TODO: Add status update here, and keep the screen here
            msg = "Failed to validate db name, or column size:\n" + str(ex)
            self.Columns = 0
            self.Name = ""
            self.ActionWidgets[0].selected = True
            self.ActionWidgets[0].Highlight()
            self.ActionWidgets[0].Active()
            return
    
    # Move on to CreateTableColumn
    def Next(self):
        return CreateTableColumns(self.Name, self.Columns)

if __name__ == "__main__":
    user = raw_input('Enter the MySQL db user: ')
    password = raw_input('Enter the MySQL db user password: ')
    host = raw_input('Enter the MySQL db host: ')
    port = raw_input('Enter the MySQL db port: ')
    database = raw_input('Enter the MySQL db database: ')
    my = MySQLConnection(user, password, host, int(port), database)    
    result = my.Connect()
    if result.Success:
        CDBCore.InitCurses()
        CDBCore.CurrentScreen = CreateTable()
        CDBCore.Connection = my
        CDBCore.Main()    
    else:
        print "Could not log in: " + result.Message