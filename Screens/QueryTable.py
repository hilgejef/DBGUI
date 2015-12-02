import sys
import curses
from CDBCore import CDBCore
from Label import Label
from Label import BaseLabel
from Button import BaseButton
from BaseScreen import BaseScreen
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
from TextBox import TextBox
from DataScreen import DataScreen

class QueryTable(BaseScreen):
    def __init__(self, dbName=""):
        if not CDBCore.Connection:
            raise Exception("No Connection object specified.")

        if dbName:
            CDBCore.Connection.CurrentDatabase = dbName
            CDBCore.Connection.QueryString("USE " + dbName)

        if not CDBCore.Connection.CurrentDatabase:
            raise Exception("No database specified.")

        BaseScreen.__init__(self, screen_type="QueryTable")

    def Init(self):
        self.DBName = CDBCore.Connection.Database

        # DBlabel = BaseLabel("Database: " + self.DBName, 4, 1, 3, , 
        #                 attr={"boxed": True, "y_offset" : 1, "x_offset": 1, "text_y_center": False, "text_x_center" : False})
        # TableLabel = BaseLabel("Table: " + self.TableName, 7, 1, 3, len("Database : " + self.DBName), 
        #                 attr={"boxed": True, "y_offset" : 1, "x_offset": 1, "text_y_center": False, "text_x_center" : False})
        # self.PassiveWidgets.append(DBlabel, TableLabel)

        queryLabel = Label("Query:", 5, 4)
        queryBox = TextBox(1, 50, 5, 12)
        queryButton = BaseButton("Submit", self.QueryMethod, 3, 8, 4, 64, attr=
            {
                'boxed' : True,
                'x_offset' : 1,
                'y_offset': 1
            }
        )

        self.PassiveWidgets.append(queryLabel)
        self.ActionWidgets.append(queryBox)
        self.ActionWidgets.append(queryButton)

    def QueryMethod(self):
        result = CDBCore.Connection.QueryString(self.ActionWidgets[0].Text)

        if result.Success:
            if len(self.ActionWidgets) == 2:
                self.ActionWidgets.append(DataScreen(result.Data))
            else:
                self.ActionWidgets[2].Result = result.Data
                self.ActionWidgets[2].LoadResult(reset=True)

        else:
            raise Exception("Query failed.")

    def ExecInput(self, inp):
        if self.CurrentWidget == 0:
            if inp in [curses.KEY_ENTER, ord('\n'), 10]:
                result = CDBCore.Connection.QueryString(self.ActionWidgets[0].Text)

                if result.Success:
                    # sys.exit(type(result.Data[1][0][0])) # FOR TESTING PURPOSES
                    # sys.exit(result.Data) # FOR TESTING PURPOSES
                    if len(self.ActionWidgets) == 1:
                        self.ActionWidgets.append(DataScreen(result.Data))
                    else:
                        self.ActionWidgets[1].Result = result.Data
                        self.ActionWidgets[1].LoadResult(reset=True)

                # TESTING PURPOSES ONLY
                else:
                    sys.exit(result.Message)

