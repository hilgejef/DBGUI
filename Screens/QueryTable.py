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
from EditField import EditField

class QueryTable(BaseScreen):
    def __init__(self, dbName="", table=""):
        if not CDBCore.Connection:
            raise Exception("No Connection object specified.")

        if dbName:
            CDBCore.Connection.Database = dbName
            CDBCore.Connection.QueryString("USE " + dbName)

        if not CDBCore.Connection.Database:
            raise Exception("No database specified.")

        self.Table = table

        BaseScreen.__init__(self, screen_type="QueryTable")

    def Init(self):
        self.DBName = CDBCore.Connection.Database

        selectLabel = Label("SELECT", 5, 4)
        selectBox = TextBox(1, 50, 5, 12)

        fromLabel = Label("FROM", 6, 4)
        fromBox = TextBox(1, 50, 6, 12)

        whereLabel = Label("WHERE", 7, 4)
        whereBox = TextBox(1, 50, 7, 12)

        queryButton = BaseButton("Submit", self.QueryMethod, 3, 8, 5, 64, attr=
            {
                'boxed' : True,
                'x_offset' : 1,
                'y_offset': 1
            }
        )

        self.PassiveWidgets += [selectLabel, fromLabel, whereLabel]
        self.ActionWidgets += [selectBox, fromBox, whereBox, queryButton]

        self.SelectBox = selectBox
        self.FromBox = fromBox
        self.WhereBox = whereBox

        self.QueryButton = queryButton
        self.DataScreen = None

    def QueryMethod(self):
        selectText = self.SelectBox.Text
        fromText = self.FromBox.Text
        whereText = self.WhereBox.Text

        if not selectText or not fromText:
            pass

        if not whereText:
            queryString = "SELECT {} FROM {}".format(selectText, fromText)
        else:
            queryString = "SELECT {} FROM {} WHERE {}".format(selectText, fromText, whereText)

        CDBCore.Connection.Table = fromText
        result = CDBCore.Connection.QueryString(queryString)

        if result.Success:
            if not self.DataScreen:
                self.ActionWidgets.append(DataScreen(result.Data, dataMethod=self.DataMethod))
                self.DataScreen = self.ActionWidgets[-1]
            else:
                self.DataScreen.Result = result.Data
                self.DataScreen.LoadResult(reset=True)

        else:
            raise Exception("Query failed.")

    def GenerateFields(self):
        resultsObj = self.DataScreen.Result
        fields = {}

        for row in resultsObj[1]:
            for idx, field in enumerate(row):
                header = resultsObj[0][idx]
                fields[header] = field

        return fields


    def DataMethod(self):
        dataX = self.DataScreen.DataX
        cursorX = self.DataScreen.CursorX

        col = self.DataScreen.Result[0][dataX + cursorX]
        fields = self.GenerateFields()

        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = EditField(allFields=fields, colToUpdate=col)
        CDBCore.CurrentScreen.Show()

