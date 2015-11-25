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

    # Constructor
    def __init__(self, lines, characters, y, x, resultsObj=None):
        BaseWidget.__init__(self, lines, characters, y, x)
        
        # position of the selector in DataTable
        self.PosY = 0                   # row
        self.PosX = 0                   # col
        
        # DataTable UI Settings independent of Results Object
        # Can update these as we choose for each DataTable Widget
        self.ColWidth = 7               # Width of each column, update as desired
        self.RowHeight = 1              # Height of each row, update as desired
        self.ColumnDelimiter = " | "    # Delimiter string between each column's data, update as desired
        
        # variables that govern table data
        # these are base values to show an empty data table
        # LoadResultsObject() will overwrite these with resultsObj data
        self.Rows = 10
        self.Columns = 10
        self.RowLabelWidth = 2

        # load data from resultsObj to be displayed
        self.LoadResultsObject(resultsObj)    # must be called upon init to set graphics for widget

        # This essentially does nothing -- the data table is not updated here,
        # until the user TABs into the widget, the class's Active method is called
        # which is just -- get this -- self.UpdateDisplay()
        # So the question is: Why?
        self.UpdateDisplay()

    # Takes ParsedResults object from MySQLConnection / PostgreSQLConnection
    # ParseResults() method
    #
    # NOTE: ParseResults() structure uses a list in the following format
    #		list[0]: list of headers
    #		list[1]: list of list of data rows
    #
    def LoadResultsObject(self, resultsObj):
    
        if resultsObj is None:
            self.ColLabels = [" " * self.ColWidth for i in range(self.Columns)]
            self.DataCells = [[" " * self.ColWidth for i in range(self.Columns)] for j in range(self.Rows)]
            self.EnableCursor = False
        else:
            # from Results Object it reads headers and then data 
            self.ColLabels = resultsObj[0]
            self.DataCells = resultsObj[1]
            self.EnableCursor = True
            self.PosY = 0
            self.PosX = 0
        
            self.Rows = len(resultsObj[1])              # number of rows
            self.Columns = len(resultsObj[1][0])        # number of columns
            self.RowLabelWidth = len(str(self.Rows))    # column for displaying row labels needs to be
                                                    # at least as wide as the number of digits
        
        # number of rows, cols needed by data table if screen size wasn't a limiting factor
        # NOTE #1: making room for borders for DataWidget should be adjusted at
        #          self.Win.Lines and self.Wins.Characters, not here
        # NOTE #2: these need to be re-computed if any object instance variables change
        self.TotalY = self.Rows * self.RowHeight + 3   # extra rows for labels, border, and scroll bar
        self.TotalX = self.Columns * (self.ColWidth + len(self.ColumnDelimiter)) + self.RowLabelWidth + len(self.ColumnDelimiter)
        self.Pad = curses.newpad(self.TotalY + 1, self.TotalX + 1)

        # upper left position of the 3 distinct portions of the pad
        self.Pad_DisplayY = self.RowHeight + 1
        self.Pad_DisplayX = self.RowLabelWidth
    
    # set delimiter between columns to a string
    def SetDelimiter(self, delimString):
        if len(delimString) < 1:
            raise ValueError("Delimiter cannot be empty string")
        else:
            self.ColumnDelimiter = delimString;
            
            # update pad X value and recreate pad
            self.TotalX = self.Columns * (self.ColWidth + len(self.ColumnDelimiter)) + self.RowLabelWidth + len(self.ColumnDelimiter)
            self.Pad = curses.newpad(self.TotalY + 1, self.TotalX + 1)
            self.UpdateDisplay()
          
    # set column width
    def SetColumnWidth(self, cw):
        if cw < 4:           # could go down to 1 but the user needs to see something
            raise ValueError("Column Width cannot be less than 4")
        else:
            self.ColWidth = cw
            self.TotalX = self.Columns * (self.ColWidth + len(self.ColumnDelimiter)) + self.RowLabelWidth + len(self.ColumnDelimiter)
            self.Pad = curses.newpad(self.TotalY + 1, self.TotalX + 1)
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
            dataText = l[:self.ColWidth]          # displays on first X chars up to ColWidth
            spaceFiller = " " * (self.ColWidth - len(dataText))
            text += dataText + spaceFiller
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
                text = self.DataCells[y][x]
                spaceFiller = " " * (self.ColWidth - len(text))
                text = text + spaceFiller
                if x == self.PosX and y == self.PosY and self.EnableCursor:
                    self.Pad.addstr(2 + y, self.RowLabelWidth + len(self.ColumnDelimiter) + (x * (self.ColWidth + len(self.ColumnDelimiter))), text, curses.A_REVERSE)
                else:
                    self.Pad.addstr(2 + y, self.RowLabelWidth + len(self.ColumnDelimiter) + (x * (self.ColWidth + len(self.ColumnDelimiter))), text, curses.A_NORMAL)
                self.Pad.addstr(2 + y, self.RowLabelWidth + len(self.ColumnDelimiter) + (x * (self.ColWidth + len(self.ColumnDelimiter))) + self.ColWidth, self.ColumnDelimiter, curses.A_NORMAL)

    def UpdatePadWindowYX(self):
        # Updates the Y, X positions of variables that determine how pad is displayed
        #
        # Upper Left of Row Labels:  self.Pad_DisplayY, 0
        # Upper Left of Column Labels:  0, self.Pad_DisplayX
        # Upper Left of Table Data:  self.Pad_DisplayY, self.Pad_DisplayX
        
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
        
        # TODO: fix -> not working properly
        # make sure displayX has not moved too far right
        if self.Pad_DisplayX > self.TotalX - data_table_chars:
            self.Pad_DisplayX = self.TotalX - data_table_chars - len(self.ColumnDelimiter) - 1
            
        # make sure displayY has not moved too far down
        # only needed if RowHeight is customizable
        
    def UpdateDisplay(self):
        #UpdateDisplay displays row numbers, column labels, and the data
        #according to values set by Pad_DisplayY and Pad_DisplayX
        
        self.UpdatePad()
        self.UpdatePadWindowYX()

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
        self.Refresh()

    def Active(self):
        self.UpdateDisplay()

    def ExecInput(self, key):
        if key in [curses.KEY_DOWN, ord('s')] and self.EnableCursor:
            if self.PosY < (self.Rows - 1):
                self.PosY += 1
                self.UpdateDisplay()
        elif key in [curses.KEY_UP, ord('w')] and self.EnableCursor:
            if self.PosY > 0:
                self.PosY -= 1
                self.UpdateDisplay()
        elif key in [curses.KEY_RIGHT, ord('d')] and self.EnableCursor:
            if self.PosX < (self.Columns - 1):
                self.PosX += 1
                self.UpdateDisplay()
        elif key in [curses.KEY_LEFT, ord('a')] and self.EnableCursor:
            if self.PosX > 0:
                self.PosX -= 1
                self.UpdateDisplay()
        elif key in [ord('\n'), 10]:    # ENTER
            #TODO: When we decide what selecting a cell should do
            pass
        else:
            pass
        