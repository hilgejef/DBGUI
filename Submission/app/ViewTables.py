###############################################################################
# ViewTables
#
# Overview: 
# 	Displays available tables
#
###############################################################################
import sys
import curses
import CDBCore
import SelectTaskScreen
from Label import Label
from Label import BaseLabel
from Button import BaseButton
from BaseScreen import BaseScreen
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
from DataScreen import DataScreen
from AlterTable import AlterTable

# _PAGESIZE_ = 5

class ViewTables(BaseScreen):
    def __init__(self, DBName=""):
        if DBName:
            CDBCore.CDBCore.Connection.Database = DBName

        elif not CDBCore.CDBCore.Connection.Database:
            raise Exception("No database selected.")

        BaseScreen.__init__(self, screen_type="ViewTables")


    def Init(self):
        self.CurrentPage = 0
        self.NumTables = 0

        self.GetTables()

        if self.ActionWidgets:
            self.ActionWidgets[0].Active()

    # Retrieves a list of tables
    def GetTables(self):
        try:
            # Retrieve a list of tables
            result = CDBCore.CDBCore.Connection.GetTables()
            
            # Ensure there weren't any issues getting the list of tables.
            if not result.Success:
                sys.exit(result.Message) # FOR TESTING

            else:
                self.Data = result.Data[1]

            # Set NumTables
            self.NumTables = len(self.Data)
            
            # Create a column of Buttons for each table
            dataScreen = DataScreen(result.Data, dataMethod=self.SendToAlter, majorScreen="ViewTables", 
                attr={
                    "start_y" : 7,
                    "column_size" : 50,
                    "display_rows" : 5
                    }
            )

            self.DataScreen = dataScreen
            self.ActionWidgets.append(dataScreen)

            if self.NumTables:
                self.PassiveWidgets.append(Label("Viewing Tables", 5, 15))
            else:
                strLabel = "No tables -- ENTER to return to Select Task"
                self.PassiveWidgets.append(Label(strLabel, 5, 15))



        except Exception as ex:
            # TODO: Add status update here
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Get tables failed") 

    # Buttons will send to Alter Table on Enter Press
    def SendToAlter(self):
        curses.ungetch('\n')

    def Next(self):
        if self.NumTables:
            table = self.DataScreen.ActionWidgets[self.DataScreen.CurrentWidget].Text

            return AlterTable(table)
        else:
            return SelectTaskScreen.SelectTaskScreen()