import sys
import curses
from CDBCore import CDBCore
from Label import BaseLabel
from Button import BaseButton
from BaseScreen import BaseScreen
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
from DataTable import DataTable

_PAGESIZE_ = 5

class ViewTables(BaseScreen):
    def __init__(self, DBName=""):
        if DBName:
            CDBCore.CurrentDatabase = DBName

        elif not CDBCore.CurrentDatabase:
            raise Exception("No database selected.")

        BaseScreen.__init__(self, screen_type="ViewTables")
            
    def Init(self):
        self.CurrentPage = 0
        self.NumTables = 0

        self.PassiveWidgets.append(BaseLabel("View Tables", 3, 13, 5, 4, 
            attr={
                "boxed" : True,
                "text_x_center" : True,
                "y_offset" : 1
            }
        ))
        self.GetTables()


    # Retrieves a list of tables
    def GetTables(self):
        try:
            # Retrieve a list of tables
            result = CDBCore.Connection.QueryString("SHOW TABLES FROM " + CDBCore.CurrentDatabase)
            
            # Ensure there weren't any issues getting the list of tables.
            if not result.Success:
                sys.exit(result.Message) # FOR TESTING

            else:
                self.Data = result.Data[1]

            # Set NumTables
            self.NumTables = len(self.Data)
            
            # Create a column of Buttons for each table
            self.AddTables()

        except Exception as ex:
            # TODO: Add status update here
            sys.exit(str(ex)) # FOR TESTING

    def AddTables(self):
            self.ActionWidgets = []
            self.PassiveWidgets = [self.PassiveWidgets[0]]

            # Create a label indicating the current Results page
            pageCount = "Page: {}".format(self.CurrentPage + 1)
            pageLabel = BaseLabel(pageCount, 3, len(pageCount) + 2, 5, 62, 
                attr = {
                    "boxed" : True,
                    "text_x_center" : True,
                    "y_offset" : 1
                }
            )

            self.PassiveWidgets.append(pageLabel)

            # Initialize table indexes based on pagesize variable
            start = self.CurrentPage * _PAGESIZE_
            end = min((self.CurrentPage + 1) * _PAGESIZE_, self.NumTables )

            # Create a button for each table 
            # Button should set the CurrentTable when activated
            for offset, name in enumerate(self.Data[start:end]):
                self.ActionWidgets.append(BaseButton(name[0], self.SetTable, 3, 40, 5 + offset * 2, 20,
                    attr={
                        "vert_border" : True,
                        "text_x_center" : True,
                        "y_offset" : 1
                    }
                ))

            # Back button goes back 1 page of results
            backButton = BaseButton("Back (B)", self.BackFunc(), 3, 10, 17, 20,
                attr={
                    "boxed" : True,
                    "text_x_center" : True,
                    "y_offset" : 1
                }
            )

            self.PassiveWidgets.append(backButton)
            self.backButton = backButton

            # Next button goes forward 1 page of results
            nextButton = BaseButton("Next (N)", self.NextFunc(), 3, 10, 17, 50,
                attr={
                    "boxed" : True,
                    "text_x_center" : True,
                    "y_offset" : 1
                }
            )

            self.PassiveWidgets.append(nextButton)
            self.nextButton = nextButton

    # Function returns a function that paginates backward
    def BackFunc(self):
        def EmptyMethod():
            pass

        def BackMethod():
            self.CurrentPage -= 1
            self.CurrentWidget = 0
            self.AddTables()
            self.MakeActive()

        if self.CurrentPage == 0:
            return EmptyMethod

        else:
            return BackMethod

    # Function returns a function that paginates forward
    def NextFunc(self):
        def EmptyMethod():
            pass

        def NextMethod():
            self.CurrentPage += 1
            self.CurrentWidget = 0
            self.AddTables()
            self.MakeActive()

        if (self.CurrentPage + 1) * _PAGESIZE_ >= self.NumTables:
            return EmptyMethod

        else:
            return NextMethod

    # ViewTables screen inputs: N for forward and B for backward
    def ExecInput(self, inp):
        if inp in [ord('n')]:
            self.nextButton.CallMethod()

        elif inp in [ord('b')]:
            self.backButton.CallMethod()

        else:
            pass

    # Sets Connection.Table to current table/advances to QueryTable
    def SetTable(self):
        pass

    # TODO: Return the next screen
    def Next(self):
        return None
