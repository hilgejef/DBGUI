import curses
from CDBCore import CDBCore
from MainMenu import MainMenu
from BaseScreen import BaseScreen
from BaseWidget import BaseWidget
from Label import Label
from TextBox import TextBox
from DataTable import DataTable

CDBCore.InitCurses(debug=True)
CDBCore.InitColor()

# label testing
lbl = Label("TestLabel", 5, 5)
txtbx = TextBox(5, 30, 7, 5)

# Test DataTable
resultsobj = [["colA", "columnB", "CCCCCCCCCCCCCCCCC", "colD"],
             [["data00", "data01", "data02", "data03"],
              ["datahereis toolong", "more data here", "row2data3", "data13"],
              ["20", "21", "22", "23"],
              ["aa", "ab", "ac", "ad"],
              ["once upon a time there was ", "test test test", "datadatadata", "allofthis is f"],
              ["", "", "", ""],
              ["last0", "last1", "last2", "last3"],
              ]]
datatbl = DataTable(8, 30, 15, 5)

screen = BaseScreen()

screen.PassiveWidgets.append(lbl)
screen.ActionWidgets.append(datatbl)
screen.ActionWidgets.append(txtbx)


datatbl.LoadResultsObject(resultsobj)

CDBCore.MenuScreen = MainMenu()
CDBCore.CurrentScreen = screen

# TEST DATA TABLE NOT APPEARING IMMEDIATELY
# CDBCore.CurrentScreen.ActionWidgets[1].Active() # Didn't fix
# CDBCore.CurrentScreen.ActionWidgets[1].UpdateDisplay() # Didn't fix
# CDBCore.CurrentScreen.ActionWidgets[0].UnHighlight() # Didn't fix
# CDBCore.CurrentScreen.NextWidget() Didn't fix

CDBCore.Main()