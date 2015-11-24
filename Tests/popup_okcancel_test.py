import sys
import curses
from CDBCore import CDBCore
from PopUp import PopUpOkCancel

def testMethod():
    pass
    
if __name__ == "__main__":
	CDBCore.InitCurses(debug=False)
	CDBCore.InitColor()
	popup = PopUpOkCancel("Test", testMethod, sys.exit)
	CDBCore.CurrentScreen = popup
	CDBCore.Main()
