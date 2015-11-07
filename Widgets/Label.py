import curses
import curses.panel
from BaseWidget import BaseWidget

""" BaseLabel """
class BaseLabel(BaseWidget):
	def __init__(self, text, l, c, y, x):
		BaseWidget.__init__(self, l, c, y, x)
		self.Text = text
		self.UpdateDisplay()

""" Label """
class Label(BaseLabel):
    def __init__(self, text, y, x):
        BaseLabel.__init__(self, text, 1, len(text) + 1, y, x)
