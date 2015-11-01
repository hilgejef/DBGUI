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
        
        # later Rows and Columns will be determined by Results Object
        # following values are arbitrary
        self.Rows = 15   # ARBITRARY NUMBER USED FOR TESTING
        self.Columns = 15   # ARBITRARY NUMBER USED FOR TESTING
        self.ColWidth = 7   # Width of each column, update as desired
        self.RowHeight = 1  # Height of each row, update as desired
        self.RowLabelWidth = len(str(self.Rows))
        self.ColumnDelimiter = " | "   # Can change delimiter string as desired 
        
        # number of rows, cols needed by data table if screen size wasn't a limiting factor
        self.TotalY = self.Rows * self.RowHeight + 3   # extra rows for labels, border, and scroll bar
        self.TotalX = self.Columns * (self.ColWidth + len(self.ColumnDelimiter)) + self.RowLabelWidth + len(self.ColumnDelimiter)
        self.Pad = curses.newpad(self.TotalY + 1, self.TotalX + 1)

        # upper left position of the 3 distinct portions of the pad
        self.Pad_DisplayY = self.RowHeight + 1
        self.Pad_DisplayX = self.RowLabelWidth
        
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
        #TODO: Update this to account for label.Text not being the same size as self.ColWidth
        text = " " * self.RowLabelWidth
        text += self.ColumnDelimiter
        for l in self.ColLabels:
            text += l.Text[:self.ColWidth]
            text += self.ColumnDelimiter
        self.Pad.addstr(0, 0, text)
        
        # Line 1: border
        self.Pad.addstr(1, 0, "-" * self.TotalX)
        
        # Lines 2 to Rows + 2: iterate through rows
        for y in range(self.Rows):
            # TODO:  account for larger number of rows than 2 digits
            self.Pad.addstr(2 + y, 0, str(y))
            self.Pad.addstr(2 + y, self.RowLabelWidth, self.ColumnDelimiter, curses.A_NORMAL)
            for x in range(self.Columns):
                text = self.DataCells[y][x].Text
                if x == self.PosX and y == self.PosY:
                    self.Pad.addstr(2 + y, self.RowLabelWidth + len(self.ColumnDelimiter) + (x * (self.ColWidth + len(self.ColumnDelimiter))), text, curses.A_REVERSE)
                else:
                    self.Pad.addstr(2 + y, self.RowLabelWidth + len(self.ColumnDelimiter) + (x * (self.ColWidth + len(self.ColumnDelimiter))), text, curses.A_NORMAL)
                self.Pad.addstr(2 + y, self.RowLabelWidth + len(self.ColumnDelimiter) + (x * (self.ColWidth + len(self.ColumnDelimiter))) + self.ColWidth, self.ColumnDelimiter, curses.A_NORMAL)

    def UpdatePadWindowYX(self):
        # Updates the Y, X positions of variables that determine how pad is displayed
        #
        # Upper Left of Row Labels:  self.PadRowLabels_DisplayY, self.PadRowLabels_DisplayX
        # Upper Left of Column Labels:  self.PadColLabels_DisplayY, self.PadColLabels_DisplayX
        # Upper Left of Table Data:  self.PadData_DisplayY, self.PadData_DisplayX
        
        data_table_lines = self.Lines - self.RowHeight - 1
        data_table_chars = self.Characters - self.RowLabelWidth
        
        # if cursor has moved lower than displayed window then move window down
        if (self.PosY * self.RowHeight) + 3 > (self.Pad_DisplayY + data_table_lines):
            self.Pad_DisplayY += self.RowHeight
            
        # if cursor has moved higher than displayed window then move window up
        if (self.PosY * self.RowHeight) + 3 <= self.Pad_DisplayY:
            self.Pad_DisplayY -= self.RowHeight
            
        # if cursor has moved to right of displayed window so that the entire column can't be displayed then move window right
        if (((self.PosX + 1) * (self.ColWidth + len(self.ColumnDelimiter))) + self.RowLabelWidth + len(self.ColumnDelimiter)) >= (self.Pad_DisplayX + data_table_chars):
            self.Pad_DisplayX += self.ColWidth + len(self.ColumnDelimiter)
        
        # if cursor has moved to left of displayed window then move window left
        if ((self.PosX * (self.ColWidth + len(self.ColumnDelimiter))) + self.RowLabelWidth + len(self.ColumnDelimiter)) < self.Pad_DisplayX:
            self.Pad_DisplayX -= self.ColWidth + len(self.ColumnDelimiter)
        
    
    def UpdateDisplay(self):
        #UpdateDisplay picks the part of the pad that the cursor is in and 
        
        self.Pad.erase()
        self.UpdatePad()
        # display row numbers
        self.Pad.refresh(
            self.Pad_DisplayY,
            0,
            self.Y + 2,
            self.X,
            self.Y + self.Lines - 1,
            self.X + self.RowLabelWidth - 1
        )
        # display col labels
        self.Pad.refresh(
            0,
            self.Pad_DisplayX,
            self.Y,
            self.X + self.RowLabelWidth,
            self.Y + self.RowHeight,
            self.X + self.Characters - 1
        )
        # display correct table data
        self.Pad.refresh(
            self.Pad_DisplayY,
            self.Pad_DisplayX,
            self.Y + self.RowHeight + 1,
            self.X + self.RowLabelWidth,
            self.Y + self.Lines - 1,
            self.X + self.Characters - 1
        )
        #self.Pad.refresh(0, 0, self.Y, self.X, self.Y + self.Lines - 1, self.X + self.Characters - 1)
        self.Refresh()

        
    def Active(self):
        capturing = True
        
        while capturing:
            key = self.Win.getch()
            
            if key in [curses.KEY_DOWN, ord('s')]:
                if self.PosY < (self.Rows - 1):
                    self.PosY += 1
                    self.UpdatePadWindowYX()
            elif key in [curses.KEY_UP, ord('w')]:
                if self.PosY > 0:
                    self.PosY -= 1
                    self.UpdatePadWindowYX()
            elif key in [curses.KEY_RIGHT, ord('d')]:
                if self.PosX < (self.Columns - 1):
                    self.PosX += 1
                    self.UpdatePadWindowYX()
            elif key in [curses.KEY_LEFT, ord('a')]:
                if self.PosX > 0:
                    self.PosX -= 1
                    self.UpdatePadWindowYX()
            elif key in [ord('\t'), 9]:     # TAB
                curses.ungetch('\t') # Notify the core that tab was pressed
                capturing = False
            
            self.UpdateDisplay()
        