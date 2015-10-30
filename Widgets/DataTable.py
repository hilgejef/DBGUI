#################################################################
# Authors:          Rich Gagliano, Jonathan Moore, Jeffrey Hilger
# Date Created:     10/26/2015
# Date Modified:    10/26/2015
# File Name:        DataTable.py
#
# Overview:
#    TODO: Project overview
#
#################################################################

import curses
import curses.panel
from BaseWidget import BaseWidget
from Label import Label


""" Data Table """
class DataTable(BaseWidget):
    def __init__(self, lines, characters, y, x):        # TODO:  add Results object in to be passed into init
        BaseWidget.__init__(self, lines, characters, y, x)
        # position of the selector
        self.PosY = 0
        self.PosX = 0
        # upper left position of the displayed portion of the pad
        self.DisplayPadY = 0
        self.DisplayPadX = 0
        
        # later Rows and Columns will be determined by Results Object
        # following values are arbitrary
        self.Rows = 3
        self.Columns = 3
        self.ColWidth = 8
        self.RowHeight = 1
        # number of rows, cols needed by data table if screen size wasn't a limiting factor
        self.TotalY = self.Rows * self.RowHeight + 3   # extra rows for labels, border, and scroll bar
        self.TotalX = self.Columns * (self.ColWidth + 1) + 4  # extra rows for row #, border, and scroll bar
        self.Pad = curses.newpad(self.TotalY + 1, self.TotalX + 1)
        
        #
        # ARBITRARY DATA FOR TESTING
        # Data in the application will come from a Results Object
        #
        
        # create labels for cells
        self.ColLabels = [Label("tstCol" + str(j), self.Y + 0, self.X + j * (self.ColWidth + 1) + 2) for j in range(self.Columns)]
        for lbl in self.ColLabels:
            lbl.Hide()
            lbl.Refresh()
        
        # create data cells that table will be composed of
        # [y, x] for positioning of data cells
        self.DataCells = [[Label("tCell" + str(i) + str(j), self.Y + i + 2, self.X + j * (self.ColWidth + 1) + 2) for i in range(self.Rows)] for j in range(self.Columns)]
        for y in range(self.Rows):
            for x in range(self.Columns):
                self.DataCells[y][x].Hide()
                self.DataCells[y][x].Refresh()

        self.UpdateDisplay()
        
    def UpdatePad(self):
        # self.Pad contains the entire graphical output of the DataTable
        
        # clear pad
        self.Pad.erase()
        
        # Line 0: column labels
        text = "  |"
        for l in self.ColLabels:
            text += l.Text
            text += "|"
        self.Pad.addstr(0, 0, text)
        
        # Line 1: border
        self.Pad.addstr(1, 0, "-" * self.TotalX)
        
        # Lines 2 to Rows + 2: iterate through rows
        for y in range(self.Rows):
            # TODO:  account for larger number of rows than 2 digits
            text = "%02d"%y + "|"
            self.Pad.addstr(2 + y, 0, text)
            for x in range(self.Columns):
                text = self.DataCells[y][x].Text
                if x == self.PosX and y == self.PosY:
                    self.Pad.addstr(2 + y, 3 + (x * self.ColWidth), text, curses.A_REVERSE)
                else:
                    self.Pad.addstr(2 + y, 3 + (x * self.ColWidth), text, curses.A_NORMAL)
                self.Pad.addstr(2 + y, 3 + (x * self.ColWidth) + self.ColWidth - 1, "|", curses.A_NORMAL)

    def UpdateDisplay(self):
        #UpdateDisplay picks the part of the pad that the cursor is in and 
        #self.UpdatePadWindow()   TODO:  creates the Y, X coordinates of the pad based on cursor location
        
        self.Pad.erase()
        self.UpdatePad()
        self.Pad.refresh(0, 0, self.Y, self.X, self.Y + self.Lines - 1, self.X + self.Characters - 1)
        self.Refresh()
        
    def UpdatePadWindow(self):
        #TODO: upon cursor move, update the portion of the pad that gets displayed
        pass
            
    def Active(self):
        
        capturing = True
        
        while capturing:
            key = self.Win.getch()
            
            if key in [curses.KEY_DOWN, ord('s')]:
                if self.PosY < (self.Rows - 1):
                    self.PosY += 1
            elif key in [curses.KEY_UP, ord('w')]:
                if self.PosY > 0:
                    self.PosY -= 1
            elif key in [curses.KEY_RIGHT, ord('d')]:
                if self.PosX < (self.Columns - 1):
                    self.PosX += 1
            elif key in [curses.KEY_LEFT, ord('a')]:
                if self.PosX > 0:
                    self.PosX -= 1
            elif key in [ord('\t'), 9]:     # TAB
                curses.ungetch('\t') # Notify the core that tab was pressed
                capturing = False
            
            self.UpdateDisplay()
        