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

import curses, sys
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
        self.TotalLabelsInScreen = 2  # number of logs displayed in screen at a time
        
        self.logLabelY = self.ScreenStartY + 1
        self.logLabelX = 30
        genLabelY = self.ScreenStartY + 1
        genLabelX = 1
        
        self.LogDisplayPos = 0      # index of self.Log to be displayed on bottom line of screen
        self.CursorPos = 0          # index of self.Log that the cursor is currently on
        self.CursorActive = False
        
        # blank widget for drawing a border around the entirety of the Status Screen
        self.PassiveWidgets.append(BaseWidget(self.ScreenHeight,
                                              CDBCore.TERMINAL_CHARACTERS,
                                              self.ScreenStartY,
                                              0))
        self.PassiveWidgets[0].Win.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.PassiveWidgets[0].ToBottom()
        
        # label widget for persistent messages
        self.PassiveWidgets.append(Label("Ctrl-T for Main Menu", genLabelY, genLabelX))
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
        
        lblIdx = self.TotalLabelsInScreen + 1   # index of first PassiveWidgets to display from top to bottom
        for msgIdx in range(min(self.TotalLabelsInScreen, len(self.Log))):
            # x width available for label messages
            charsAvailable = CDBCore.TERMINAL_CHARACTERS - self.logLabelX - 2
            lblMsg = self.Log[msgIdx + self.LogDisplayPos][:charsAvailable]
            fillerChars = charsAvailable - len(lblMsg)
            lblMsg += (" " * fillerChars)
            # clear and redraw the label
            self.PassiveWidgets[lblIdx].Win.erase()
            self.PassiveWidgets[lblIdx] = Label(lblMsg, self.logLabelY + lblIdx - 2, self.logLabelX)
            # HIGHLIGHT TEXT if the label is the current cursor position, and messages are being scrolled
            if self.CursorActive and self.CursorPos == msgIdx + self.LogDisplayPos:
                self.PassiveWidgets[lblIdx].Highlight()
            self.PassiveWidgets[lblIdx].ToTop()
            lblIdx -= 1
        self.Show()
        
    def UpdatePersistentMessage(self, msgString):
        # updates the persistent message screen
        self.PassiveWidgets[1] = Label(msgString[:self.logLabelX - 4], self.logLabelY, self.logLabelX)
        self.PassiveWidgets[1].ToTop()
        self.Show()
        
    def MessageScroll(self):
        self.CursorActive = True
        self.UpdateLogLabels()
        
        while self.CursorActive:
            currentLabelIndex = 1 + self.TotalLabelsInScreen - (self.CursorPos - self.LogDisplayPos)
            try:
                key = self.PassiveWidgets[currentLabelIndex].Win.getch()
            except:
                print "currentLabelIndex = ", currentLabelIndex
                print "self.CursorPos = ", self.CursorPos
                print "self.LogDisplayPos = ", self.LogDisplayPos
                sys.exit()
            
            if key in [curses.KEY_DOWN, ord('s')]:
                if self.CursorPos > 0:
                    self.CursorPos -= 1
                    if self.LogDisplayPos > self.CursorPos:
                        self.LogDisplayPos = self.CursorPos
                self.UpdateLogLabels()
            elif key in [curses.KEY_UP, ord('w')]:
                if self.CursorPos < (len(self.Log) - 1):
                    self.CursorPos += 1
                    if self.LogDisplayPos < self.CursorPos - self.TotalLabelsInScreen + 1:
                        self.LogDisplayPos += 1
                self.UpdateLogLabels()
            elif key in [ord('\t'), 9]:     # TAB
                # exit for screen
                self.CursorPos = 0
                self.CursorActive = False
                self.UpdateLogLabels()
                return
            elif key in [ord('\n'), 10]:    # ENTER
                #TODO: When a message is selected it should call a popup screen that displays the full message
                pass
        
        
        