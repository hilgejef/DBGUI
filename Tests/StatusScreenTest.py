import curses

from CDBCore import CDBCore
from StatusScreen import StatusScreen

CDBCore.InitCurses()
statusScreen = StatusScreen()
statusScreen.AddStatusMessage("Test Message 1")
statusScreen.AddStatusMessage("Test Message 2.  This one is supposed to go really far across the screen")
statusScreen.AddStatusMessage("Test Msg 3. Does scrolling work?")
statusScreen.AddStatusMessage("More messages")
statusScreen.MessageScroll()
CDBCore.CleanupCurses()
