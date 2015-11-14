###############################################################################
# Author:		    Jonathon Moore
# Date Created:		11/13/2015
# Date Modified:	11/13/2015
# File Name:		StatusScreen.py
#
# Overview:         StatusScreen displays messages from the system to the user
#                   in a scrolling log format.
#
###############################################################################

import curses
from CDBCore import CDBCore
from BaseWidget import BaseWidget
from Label import Label
from BaseScreen import BaseScreen

class StatusScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
        
    def Init(self):
        # log for status messages, array of strings
        self.Log = []
        
        # screen settings & spacing variables
        self.ScreenStartY = 20
        self.ScreenHeight = 4       # Status Screen will be 4 tiles high including it's border
        self.TotalLabelsInScreen = 2
        
        self.logLabelY = self.ScreenStartY + 1
        self.logLabelX = 30
        genLabelY = self.ScreenStartY + 1
        genLabelX = 1
        
        # blank widget for drawing a border around the entirety of the Status Screen
        self.PassiveWidgets.append(BaseWidget(self.ScreenHeight,
                                              CDBCore.TERMINAL_CHARACTERS,
                                              self.ScreenStartY,
                                              0))
        self.PassiveWidgets[0].Win.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.PassiveWidgets[0].ToBottom()
        
        # label widget for persistent messages
        self.PassiveWidgets.append(Label("Ctrl-M for Main Menu", genLabelY, genLabelX))
        self.PassiveWidgets[1].ToTop()
        
        # label widgets for logged system messages
        for y in range(0, self.TotalLabelsInScreen):
            self.PassiveWidgets.append(Label(" " * (CDBCore.TERMINAL_CHARACTERS - self.logLabelX - 2),
                                             self.logLabelY + y,
                                             self.logLabelX))
            self.PassiveWidgets[y + 2].ToTop()
        self.Show()
        
    def AddStatusMessage(self, msgString):
        # put new message at beginning of list
        self.Log.insert(0, msgString)
        self.UpdateLogLabels()
        
    def UpdateLogLabels(self):
        # updates the labels on screen to show the last X messages
        # PassiveWidgets[0] = screen border
        # PassiveWidgets[1] = Persistent Messaging
        # PassiveWidgets[2..X] = Log Labels, from top to bottom.
        # PassiveWidgets[X] holds most recent message, [X-1] next most recent, etc.
        
        # if self.Log is empty do nothing
        if not self.Log:
            return
        
        lblIdx = self.TotalLabelsInScreen + 1
        for msgIdx in range(min(self.TotalLabelsInScreen, len(self.Log))):
            lblMsg = self.Log[msgIdx][:CDBCore.TERMINAL_CHARACTERS - self.logLabelX - 2]
            self.PassiveWidgets[lblIdx] = Label(lblMsg, self.logLabelY + lblIdx - 2, self.logLabelX)
            self.PassiveWidgets[lblIdx].ToTop()
            lblIdx -= 1
        self.Show()
        
    def UpdatePersistentMessage(self, msgString):
        # updates the persistent message screen
        self.PassiveWidgets[1] = Label(msgString[:self.logLabelX - 4], self.logLabelY, self.logLabelX)
        self.PassiveWidgets[1].ToTop()
        self.Show()