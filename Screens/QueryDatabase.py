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

class QueryDatabase(BaseScreen):
    def __init__(self, dbName="", table=""):
        if not CDBCore.CDBCore.Connection:
            raise Exception("No Connection object specified.")

        if dbName:
            CDBCore.CDBCore.Connection.Database = dbName
            CDBCore.CDBCore.Connection.QueryString("USE {}".format(CDBCore.CDBCore.Connection.Database))

        if not CDBCore.CDBCore.Connection.Database:
            raise Exception("No database specified.")

        self.Table = table

        BaseScreen.__init__(self, screen_type="QueryTable")

    def Init(self):
        self.DBName = CDBCore.CDBCore.Connection.Database

        queryLabel = Label("Query:", 5, 4)
        queryBox = TextBox(1, 50, 5, 12)

        queryButton = BaseButton("Submit", self.QueryMethod, 3, 8, 5, 64, attr=
            {
                'boxed' : True,
                'x_offset' : 1,
                'y_offset': 1
            }
        )

        self.PassiveWidgets += [queryLabel]
        self.ActionWidgets += [queryBox, queryButton]

        self.QueryBox = queryBox
        self.QueryButton = queryButton
        self.DataScreen = None

    def QueryMethod(self):
        queryText = self.QueryBox.Text

        # ENSURE ALL CASES ARE TAKEN CARE OF:
        # EMPTY QUERY
        # FAILED QUERY
        # EMPTY RESULT
        # RESULT FIELDS ARE EMPTY
        # RESULT FIELDS NOT EMPTY

        # EMPTY QUERY
        if not queryText:
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("No query entered.")

            if self.DataScreen:
                self.EmptyData()

        else:
            result = CDBCore.CDBCore.Connection.QueryString(queryText)

            if result.Success:
                CDBCore.CDBCore.StatusScreen.AddStatusMessage("Query successful.")

                if result.Data:
                    # RESULT FIELDS NOT EMPTY
                    if result.Data[1]:
                        if not self.DataScreen:
                            self.ActionWidgets.append(DataScreen(result.Data, dataMethod=None))
                            self.DataScreen = self.ActionWidgets[-1]
                        else:
                            if self.PassiveWidgets[-1].Type == "DataScreen":
                                self.ActionWidgets.append(self.PassiveWidgets.pop())
                            self.DataScreen.Result = result.Data
                            self.DataScreen.LoadResult(reset=True)
                    # RESULT FIELDS ARE EMPTY
                    else:
                        if not self.DataScreen:
                            self.PassiveWidgets.append(DataScreen(result.Data, dataMethod=None))
                            self.DataScreen = self.PassiveWidgets[-1]
                        else:
                            if self.ActionWidgets[-1].Type == "DataScreen":
                                self.PassiveWidgets.append(self.ActionWidgets.pop())
                                self.DataScreen.Result = result.Data
                                self.DataScreen.LoadResult(reset=True)
                            elif self.PassiveWidgets[-1].Type == "DataScreen":
                                self.DataScreen.Result = result.Data
                                self.DataScreen.LoadResult(reset=True)
                # EMPTY RESULT
                else:
                    self.EmptyData()
            # FAILED QUERY
            else:
                self.EmptyData()

                CDBCore.CDBCore.StatusScreen.AddStatusMessage("Query failed.")

        # Maintain active state on button
        self.MakeActive()

    def EmptyData(self):
        if self.DataScreen:
            if self.ActionWidgets[-1].Type == "DataScreen":
                self.ActionWidgets.pop()
            elif self.PassiveWidgets[-1].Type == "DataScreen":
                self.PassiveWidgets.pop()
            self.DataScreen.Hide()
            self.DataScreen = None

    # def GenerateFields(self):
    #     resultsObj = self.DataScreen.Result
    #     fields = {}

    #     dataY = self.DataScreen.DataY
    #     cursorY = self.DataScreen.CursorY

    #     for idx, field in enumerate(resultsObj[1][dataY + cursorY]):
    #         header = resultsObj[0][idx]
    #         fields[header] = field

    #     return fields


    # def DataMethod(self):
    #     dataX = self.DataScreen.DataX
    #     cursorX = self.DataScreen.CursorX

    #     col = self.DataScreen.Result[0][dataX + cursorX]
    #     fields = self.GenerateFields()

    #     CDBCore.History.append(CDBCore.CurrentScreen)
    #     CDBCore.CurrentScreen.Clear()
    #     CDBCore.CurrentScreen = EditField(allFields=fields, colToUpdate=col)
    #     CDBCore.CurrentScreen.Show()
