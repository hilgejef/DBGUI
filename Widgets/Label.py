import curses
import curses.panel
from BaseWidget import BaseWidget

""" BaseLabel """
class BaseLabel(BaseWidget):
	def __init__(self, text, l, c, y, x, boxed=False, color_pair=1):
		BaseWidget.__init__(self, l, c, y, x, boxed, color_pair)
		self.Text = text

""" Label """
class Label(BaseLabel):
    def __init__(self, text, y, x):
        BaseLabel.__init__(self, text, 1, len(text) + 1, y, x)
