import sys
import curses
import CDBCore
from Label import Label
from Label import BaseLabel
from Button import BaseButton
from BaseScreen import BaseScreen
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
from TextBox import TextBox
from DataScreen import DataScreen
from EditField import EditField

""" Alter Table """
class AlterTable(BaseScreen):
    def __init__(self, table, dbName=""):
        if not CDBCore.CDBCore.Connection:
            raise Exception("No Connection object specified.")

        if dbName:
            CDBCore.CDBCore.Connection.Database = dbName
            CDBCore.CDBCore.Connection.QueryString("USE " + dbName)

        if not CDBCore.CDBCore.Connection.Database:
            raise Exception("No database specified.")

        self.Table = table

        BaseScreen.__init__(self, screen_type="QueryTable")

    def Init(self):
        result = CDBCore.CDBCore.Connection.QueryString("DESCRIBE {};".format(self.Table))

        if not result.Success:
            raise Exception(self.Table)

        self.Result = self.ModifyResult(result.Data)

        # -- MAIN ALTER SCREEN --

        tableLabel = Label("TABLE: " + self.Table, 5, 5)

        alterScreen = DataScreen(self.Result, dataMethod=[self.AlterMethod, self.DropColMethod],
            majorScreen="AlterTable", 
            attr=
                {
                    "start_y" : 7,
                    "start_x" : 5
                }
        )

        # -- ADD COL SECTION --

        addColLabel = Label("COLNAME:", 5, 50)
        addTypeLabel = Label("COLTYPE:", 6, 50)

        addColTextBox = TextBox(1, 14, 5, 59)
        addTypeTextBox = TextBox(1, 14, 6, 59)

        self.ColBox = addColTextBox
        self.TypeBox = addTypeTextBox

        addButton = BaseButton("Add Col", self.AddColMethod, 3, len("Add Col") +  2, 8, 50,
            attr={
                "boxed" : True,
                "x_offset" : 1,
                "y_offset" : 1
            }
        )

        # -- DROP TABLE SECTION --

        dropButton = BaseButton("Drop Table", self.DropTblMethod, 3, len("Drop Table") + 2, 13, 50,
            attr={
                "boxed" : True,
                "y_offset" : 1,
                "x_offset" : 1
            }
        )

        # submitButton = BaseButton("Submit", self.AlterMethod, 3, 8, 14, 65, attr=
        #     {
        #         'boxed' : True,
        #         'x_offset' : 1,
        #         'y_offset': 1
        #     }
        # )

        self.PassiveWidgets += [tableLabel, addColLabel, addTypeLabel]
        self.ActionWidgets += [alterScreen, addColTextBox, addTypeTextBox, addButton, dropButton]
        self.AlterScreen = alterScreen

    # Modifies MySQL result display
    def ModifyResult(self, result):
        newResult = []

        # Create new headers
        headers = ["Field", "Type", "", ""]
        newResult.append(headers)

        newFields = []
        for row in result[1]:
            newRow = []
            for idx, field in enumerate(row[:2]):
                newRow.append(field)
            newRow.append("MOD COL")
            newRow.append("DROP COL")
            newFields.append(newRow)
        newResult.append(newFields)

        return newResult

    def AddColMethod(self):
        colName = self.ColBox.Text
        colType = self.TypeBox.Text

        q = "ALTER TABLE {} ADD {} {};".format(self.Table, colName, colType)

        result = CDBCore.CDBCore.Connection.QueryString(q)

        if result.Success:
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Add Col success")

            q = "DESCRIBE {};".format(self.Table)
            result = CDBCore.CDBCore.Connection.QueryString(q)
            resultData = self.ModifyResult(result.Data) 

            self.AlterScreen.Result = resultData
            self.AlterScreen.LoadAlterTable(reset=True)
        else:
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Add Col failed")


    def AlterMethod(self):
        rowNum = self.AlterScreen.ActionWidgets[self.AlterScreen.CurrentWidget].Row
        row = self.AlterScreen.AlterWidgets[rowNum]

        colName = row[0].Text
        colType = row[1].Text

        q = "ALTER TABLE {} MODIFY COLUMN {} {};".format(self.Table, colName, colType)
        result = CDBCore.CDBCore.Connection.QueryString(q)

        if result.Success:
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Modify Col success")

            q = "DESCRIBE {};".format(self.Table)
            result = CDBCore.CDBCore.Connection.QueryString(q)
            resultData = self.ModifyResult(result.Data) 

            self.AlterScreen.Result = resultData
            self.AlterScreen.LoadAlterTable(reset=True)
        else:
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Modify Col failed")

    def DropColMethod(self):
        rowNum = self.AlterScreen.ActionWidgets[self.AlterScreen.CurrentWidget].Row
        row = self.AlterScreen.AlterWidgets[rowNum]

        colName = row[0].Text

        q = "ALTER TABLE {} DROP COLUMN {};".format(self.Table, colName)

        result = CDBCore.CDBCore.Connection.QueryString(q)

        if result.Success:
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Drop Col success")

            q = "DESCRIBE {};".format(self.Table)
            result = CDBCore.CDBCore.Connection.QueryString(q)
            resultData = self.ModifyResult(result.Data) 

            self.AlterScreen.Result = resultData
            self.AlterScreen.LoadAlterTable(reset=True)
        else:
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Drop Col failed")

    def DropTblMethod(self):
        q = "DROP TABLE {};".format(self.Table)

        result = CDBCore.CDBCore.Connection.QueryString(q)

        if result.Success:
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Drop Table success")

            resultData = (["Field", "Type", "", ""], [])

            self.AlterScreen.Result = resultData
            self.AlterScreen.LoadAlterTable(reset=True)
        else:
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Drop Table failed")


    # def GenerateFields(self):
    #     resultsObj = self.DataScreen.Result
    #     fields = {}

    #     dataY = self.DataScreen.DataY
    #     cursorY = self.DataScreen.CursorY

    #     for idx, field in enumerate(resultsObj[1][dataY + cursorY]):
    #         header = resultsObj[0][idx]
    #         fields[header] = field

    #     return fields
