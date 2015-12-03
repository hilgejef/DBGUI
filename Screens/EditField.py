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

# allFields = dictionary of header : field value
# colToUpdate = name of col that is to be updated
""" EditField """
class EditField(BaseScreen):
    def __init__(self, allFields, colToUpdate, table=None):
        self.AllFields = allFields
        self.colToUpdate = colToUpdate

        if not table and not CDBCore.Connection.Table:
            raise Exception("No table specified")

        elif table:
            CDBCore.Connection.Table = table

        BaseScreen.__init__(self, screen_type="EditField")

    def Init(self):
        currentDb = CDBCore.Connection.Database
        currentTbl = CDBCore.Connection.Table
        currentCol = self.colToUpdate

        fieldLabel = Label("Field Value: ", 5, 5)

        fieldBox = TextBox(1, 40, 5, len("Field Value: ") + 5)

        fieldButton = BaseButton("Submit", self.UpdateMethod, 3, len("Submit") + 2, 4, 
                                 45 + len("Field Value") + 1, attr={
                                    "boxed" : True,
                                    "y_offset" : 1,
                                    "x_offset" : 1
                                 }) 

        dbLabel = BaseLabel("Database: " + currentDb, 2, len("Database: " + currentDb) + 2, 8, 5,
            attr={
                "bottom_border" : True,
                "x_offset" : 1
            }
        )
        tableLabel = BaseLabel("Table: " + currentTbl, 2, len("Table: " + currentTbl) + 2, 11, 5,
            attr={
                "bottom_border" : True,
                "x_offset" : 1
            }
        )

        colLabel = BaseLabel("Column: " + currentCol, 2, len("Column: " + currentCol) + 2, 14, 5,
            attr={
                "bottom_border" : True,
                "x_offset" : 1
            }
        )

        result = CDBCore.Connection.QueryString(self.MakeSelectString())

        whereFields = DataScreen(result.Data, attr={"start_y" : 17, "start_x" : 19})
        self.WhereFields = whereFields

        self.PassiveWidgets += [fieldLabel, dbLabel, tableLabel, colLabel]
        self.ActionWidgets += [fieldBox, fieldButton, whereFields]

    def MakeSelectString(self):
        selectString = "SELECT * FROM {} WHERE ".format(CDBCore.Connection.Table)
        colStrings = []

        for col in self.AllFields:
            if isinstance(self.AllFields[col], unicode) or isinstance(self.AllFields[col], str):
                colStrings.append("{} = '{}'".format(col, self.AllFields[col]))
            elif type(self.AllFields[col]) is int:
                colStrings.append("{} = {}".format(col, self.AllFields[col]))

        selectString += " AND ".join(colStrings) + " LIMIT 1;"

        return selectString

    def MakeUpdateString(self, newFieldValue):
        updateString = "UPDATE {} SET {} = {} WHERE ".format(CDBCore.Connection.Table, 
                                                             self.colToUpdate, newFieldValue)
        colStrings = []

        for col in self.AllFields:
            if isinstance(self.AllFields[col], unicode) or isinstance(self.AllFields[col], str):
                colStrings.append("{} = '{}'".format(col, self.AllFields[col]))
            elif type(self.AllFields[col]) is int:
                colStrings.append("{} = {}".format(col, self.AllFields[col]))

        updateString += " AND ".join(colStrings) + " LIMIT 1;"

        return updateString
        
    def UpdateMethod(self):
        updateValue = self.ActionWidgets[0].Text
        updateQuery = self.MakeUpdateString(updateValue)

        result = CDBCore.Connection.QueryString(updateQuery)

        if result.Success:
            self.whereFields.loadResult(result.Data)






