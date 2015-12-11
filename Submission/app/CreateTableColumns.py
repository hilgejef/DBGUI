###############################################################################
# CreateTableColumns
#
# Allows user to enter column names/types and then creates table
#
###############################################################################

import sys
import curses
import CDBCore
from Label import Label
from TextBox import TextBox
from Button import Button
from BaseScreen import BaseScreen
from CheckBox import CheckBox
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
import SelectTaskScreen

class CreateTableColumns(BaseScreen):
    def __init__(self, name, columns):
        self.Name = name
        self.Columns = columns
        BaseScreen.__init__(self)
        
    def Init(self):
        # Spacing
        yoffset = 0
        ystart = 2
        xlabel = 3
        xaction = 6
      
        # Tracking variables for retrieving entries
        self.Fields = ["ColumnName", "ColumnType"]
        for c in range(self.Columns):
            y = (c * 2) + CDBCore.CDBCore.MAIN_SCREEN_Y + 4
            xl = xlabel
            xa = xaction
            if y >= 17:
                y = (c * 2) - 10 + CDBCore.CDBCore.MAIN_SCREEN_Y + 4
                xl = xlabel + 40
                xa = xaction + 40
            self.PassiveWidgets.append(Label(str(c), y, xl))
            for f in self.Fields:
                self.ActionWidgets.append(TextBox(1, 16, y, xa))
                xa += 20
            yoffset += 3
            xaction = 6
        
        self.PassiveWidgets.append(Label("Column Name", CDBCore.CDBCore.MAIN_SCREEN_Y + 2, 7))
        self.PassiveWidgets.append(Label("Column Type", CDBCore.CDBCore.MAIN_SCREEN_Y + 2, 27))
        if self.Columns > 5:
            self.PassiveWidgets.append(Label("Column Name", CDBCore.CDBCore.MAIN_SCREEN_Y + 2, 47))
            self.PassiveWidgets.append(Label("Column Type", CDBCore.CDBCore.MAIN_SCREEN_Y + 2, 67))
            self.ActionWidgets.append(Button("Create", self.CreateTable, CDBCore.CDBCore.STATUS_SCREEN_Y - 4, 37))
        else:
            self.ActionWidgets.append(Button("Create", self.CreateTable, CDBCore.CDBCore.STATUS_SCREEN_Y - 4, 18))

    # Dynamically constructs the query to be executed
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
    
    # Creates the specified table within the DB
    def CreateTable(self):
        try:
            # Construct the create table query from the user's input
            query = self.ConstructQuery()
            
            # Attempt to create the table
            result = CDBCore.CDBCore.Connection.QueryString(query)
            
            # Ensure that the query was successful
            if not result.Success:
                raise Exception(result.Message)
            
            # Notify of successful
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Successfully created table: " + self.Name)
            
            # Move on to next screen
            curses.ungetch('\n')
            
        except Exception as ex:
            # TODO: Add multi-line once status supports it
            msg = "Failed to create table:" + self.Name
            CDBCore.CDBCore.StatusScreen.AddStatusMessage(msg)
            self.ActionWidgets[0].selected = True
            self.ActionWidgets[0].Highlight()
            self.ActionWidgets[0].Active()
            return
        
    # Go back to the selection screen
    def Next(self):
        return SelectTaskScreen.SelectTaskScreen()

# STANDALONE TESTING
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
        CDBCore.CDBCore.InitCurses()
        CDBCore.CDBCore.CurrentScreen = CreateTableColumns(name, int(columns))
        CDBCore.CDBCore.Connection = my
        CDBCore.CDBCore.Main()    
    else:
        print "Could not log in: " + result.Message        