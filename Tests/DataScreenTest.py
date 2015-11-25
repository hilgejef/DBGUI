import curses
from CDBCore import CDBCore
from MainMenu import MainMenu
from DataScreen import DataScreen

CDBCore.InitCurses(debug=True)
CDBCore.InitColor()

# Test DataTable
resultsObj = [["colA", "columnB", "CCCCCCCCCCCCCCCCC", "colD"],
             [["data00", "data01", "data02", "data03"],
              ["datahereis toolong", "more data here", "row2data3", "data13"],
              ["20", "21", "22", "23"],
              ["aa", "ab", "ac", "ad"],
              ["once upon a time there was ", "test test test", "datadatadata", "allofthis is f"],
              ["", "", "", ""],
              ["last0", "last1", "last2", "last3"]]]

# CDBCore.MenuScreen = MainMenu()
CDBCore.CurrentScreen = DataScreen(resultsObj)

# TEST DATA TABLE NOT APPEARING IMMEDIATELY
# CDBCore.CurrentScreen.ActionWidgets[1].Active() # Didn't fix
# CDBCore.CurrentScreen.ActionWidgets[1].UpdateDisplay() # Didn't fix
# CDBCore.CurrentScreen.ActionWidgets[0].UnHighlight() # Didn't fix
# CDBCore.CurrentScreen.NextWidget() Didn't fix

CDBCore.Main()