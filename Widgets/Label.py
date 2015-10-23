import curses
import curses.panel
from BaseWidget import BaseWidget

""" Label """
class Label(BaseWidget):
    def __init__(self, text, y, x):
        BaseWidget.__init__(self, 1, len(text) + 1, y, x)
        self.Text = text
        self.TextMode = curses.A_NORMAL
        self.UpdateDisplay()
    
    # Updates the display with the current text mode
    def UpdateDisplay(self):
        self.Win.erase()
        self.Win.addstr(self.Text, self.TextMode)
        self.Refresh()
    
    # Highlights the text by reversing the foreground/background
    def Highlight(self):
        self.TextMode = curses.A_REVERSE
        self.UpdateDisplay()
    
    # UnHighlights the text by setting foreground/background to current
    # terminal colors
    def UnHighlight(self):
        self.TextMode = curses.A_NORMAL
        self.UpdateDisplay()