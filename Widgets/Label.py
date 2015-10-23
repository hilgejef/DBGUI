import curses
import curses.panel
from BaseWidget import BaseWidget

""" Label """
class Label(BaseWidget):
    def __init__(self, text, y, x):
        BaseWidget.__init__(self, 1, len(text) + 1, y, x)
        self.Text = text
        self.UpdateDisplay()