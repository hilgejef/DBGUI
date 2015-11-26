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

data = [['id', 'firstname', 'lastname', 'email'], [(1, u'Jeff', u'Hilger', u'hilger@test.com'), (2, u'Jon', u'Moore', u'jon@test.com'), (3, u'Richard', u'Gagliano', u'rich@test.com')]]

dataCopy = data[:]

for idx, header in enumerate(dataCopy[0]):
    data[0][idx] = str(header)

for ridx, row in enumerate(dataCopy[1]):
    for fidx, field in enumerate(row):
        data[1][ridx][fidx] = str(field)

# CDBCore.MenuScreen = MainMenu()
CDBCore.CurrentScreen = DataScreen(data)

CDBCore.Main()