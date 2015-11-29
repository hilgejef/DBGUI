from CDBCore import CDBCore

CDBCore.InitCurses()
CDBCore.InitScreens()
CDBCore.StatusScreen.AddStatusMessage("Test Message 1")
CDBCore.StatusScreen.AddStatusMessage("Test Message 2.  This one is supposed to go really far across the screen")
CDBCore.StatusScreen.AddStatusMessage("Test Msg 3. Does scrolling work?")
CDBCore.StatusScreen.AddStatusMessage("More messages")
CDBCore.StatusScreen.MakeActive()
CDBCore.CleanupCurses()
