import curses
import curses.panel
from Label import BaseLabel
from Button import BaseButton
from BaseScreen import BaseScreen

# Data Screen is an intermediary between Widget and Screen
# that allows a collection of Widgets to emulate a data table Widget
""" DataScreen """
class DataScreen(BaseScreen):

    default_attributes = {
        "start_y" : 6,
        "start_x" : 15,
        "column_size" : 10, # Not below 3 if bordered
        "display_cols" : 5,
        "display_rows" : 5,
        "header_border" : False,
        "field_border" : True   
    }

    def __init__(self, resultsObj, dataMethod=None, attr=None):
        if dataMethod:
            self.DataMethod = dataMethod
        else:
            self.DataMethod = self.EmptyMethod

        if attr:
            merged_attributes = DataScreen.default_attributes.copy()
            merged_attributes.update(attr)
            self.Attr = merged_attributes
        else:
            self.Attr = DataScreen.default_attributes

        self.Result = resultsObj

        BaseScreen.__init__(self, screen_type="DataScreen")

        self.LoadResult()

    def Init(self):
        self.StartX = self.Attr["start_x"]
        self.StartY = self.Attr["start_y"]
        self.ColSize = self.Attr["column_size"]
        self.HeadBorder = self.Attr["header_border"]
        self.FieldBorder = self.Attr["field_border"]
        self.TotalCols = len(self.Result[0])
        self.TotalRows = len(self.Result[1])
        self.DisplayCols = min(self.TotalCols, self.Attr["display_cols"])
        self.DisplayRows = min(self.TotalRows, self.Attr["display_rows"])
        self.DataX = 0
        self.DataY = 0
        self.CursorX = 0
        self.CursorY = 0

    def LoadResult(self, reset=False):
        if reset:
            self.TotalCols = len(self.Result[0])
            self.TotalRows = len(self.Result[1])
            self.DisplayCols = min(self.TotalCols, self.Attr["display_cols"])
            self.DisplayRows = min(self.TotalRows, self.Attr["display_rows"])
            self.DataX = 0
            self.DataY = 0
            self.CursorX = 0
            self.CursorY = 0  
            self.CurrentWidget = 0          

        # Empty widget containers
        self.PassiveWidgets = []
        self.ActionWidgets = []

        # Define padding variables based on border attributes
        if self.HeadBorder:
            self.HeadPadding = 2
        else:
            self.HeadPadding = 1

        if self.FieldBorder:
            self.FieldPadding = 2
        else:
            self.FieldPadding = 1

        # Iterate through self.Result to create header labels
        for xidx, x in enumerate(range(self.DataX, min(self.TotalCols, self.DataX + self.DisplayCols))):

            # Define header attributes
            headerX = self.StartX + (self.ColSize + self.HeadPadding) * xidx
            headerY = self.StartY
            headerHeight = self.HeadPadding + 1
            headerWidth = self.ColSize

            # Ensure that text is string
            headerText = str(self.Result[0][x])[:self.ColSize - self.HeadPadding]

            if self.HeadBorder:
                attr = {
                    "boxed" : True,
                    "y_offset" : 1,
                    "x_offset" : 1,
                    "text_x_center" : True
                }
            else:
                attr = {
                    "text_x_center" : True
                }

            # Create label based on defined attributes
            headerLabel = BaseLabel(headerText, headerHeight, headerWidth, headerY, headerX, attr)

            # Add header label to passive widgets
            self.PassiveWidgets.append(headerLabel)

        # Iterate through self.Result to create field buttons
        for xidx, x in enumerate(range(self.DataX, min(self.TotalCols, self.DataX + self.DisplayCols))):
            for yidx, y in enumerate(range(self.DataY, min(self.TotalRows, self.DataY + self.DisplayRows))):

                # Define field attributes
                fieldX = self.StartX + (self.ColSize + self.HeadPadding) * xidx
                fieldY = self.StartY + (self.HeadPadding + 1) + (self.FieldPadding + 1) * yidx
                fieldHeight = self.FieldPadding + 1
                fieldWidth = self.ColSize
                fieldText = str(self.Result[1][y][x])[:self.ColSize - self.FieldPadding]
                fieldMethod = self.DataMethod

                if self.FieldBorder:
                    attr = {
                        "boxed" : True,
                        "y_offset" : 1,
                        "x_offset" : 1,
                    }
                else:
                    attr = {

                    }

                # Create button based on defined attributes
                fieldButton = BaseButton(fieldText, fieldMethod, fieldHeight, fieldWidth, fieldY, fieldX, attr)

                # Add field button to action widgets
                self.ActionWidgets.append(fieldButton)

    def Active(self):
        if self.ActionWidgets:
            self.ActionWidgets[self.CurrentWidget].Highlight()

    # Clear exec base
    def ExecBase(self, inp):
        pass

    # Load with WASD/arrow-key movement
    def ExecInput(self, key):
        # Down key action
        if key in [curses.KEY_DOWN, ord('s')]:
            if self.CursorY == self.DisplayRows - 1 and (self.DataY + self.DisplayRows - 1) == self.TotalRows - 1:
                pass
            elif self.CursorY == self.DisplayRows - 1:
                self.DataY += 1
                self.LoadResult()
                self.SetCurrent()
            else:
                self.CursorY += 1
                self.SetCurrent()

        # Up key action
        elif key in [curses.KEY_UP, ord('w')]:
            if self.CursorY == 0 and self.DataY == 0:
                pass
            elif self.CursorY == 0:
                self.DataY -= 1
                self.LoadResult()
                self.SetCurrent()
            else:
                self.CursorY -= 1
                self.SetCurrent()

        # Right key action
        elif key in [curses.KEY_RIGHT, ord('d')]:
            if self.CursorX == self.DisplayCols - 1 and (self.DataX + self.DisplayCols - 1) == self.TotalCols - 1:
                pass
            elif self.CursorX == self.DisplayCols - 1:
                self.DataX += 1
                self.LoadResult()
                self.SetCurrent()
            else:
                self.CursorX += 1
                self.SetCurrent()

        # Left key action
        elif key in [curses.KEY_LEFT, ord('a')]:
            if self.CursorX == 0 and self.DataX == 0:
                pass
            elif self.CursorX == 0:
                self.DataX -= 1
                self.LoadResult()
                self.SetCurrent()
            else:
                self.CursorX -= 1
                self.SetCurrent()

    # Empty method that can be passed to fieldButton
    def EmptyMethod(self):
        pass

    # Helper function determines Current Widget/Field
    def SetCurrent(self):
        if self.ActionWidgets:
            self.ActionWidgets[self.CurrentWidget].UnHighlight()
            self.CurrentWidget = self.CursorY + self.CursorX * self.DisplayRows
            self.ActionWidgets[self.CurrentWidget].Highlight()



