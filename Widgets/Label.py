import curses
import curses.panel
from BaseWidget import BaseWidget

""" Label """
class Label(BaseWidget):
    def __init__(self, text, y, x):
        BaseWidget.__init__(self, 3, len(text) + 5, y, x)
        self.Win.addstr(text)
        self.Refresh()