import curses
import curses.panel
from BaseWidget import BaseWidget

""" BaseLabel """
class BaseLabel(BaseWidget):
	def __init__(self, text, height, width, y, x, boxed=False, center=False, text_color=1, bkgd_color=2,
                 y_offset=0, x_offset=0):
		BaseWidget.__init__(self, height, width, y, x, boxed, center, text_color, bkgd_color,
			                y_offset, x_offset)
		self.Text = text
		self.UpdateDisplay()

""" Label """
class Label(BaseLabel):
    def __init__(self, text, y, x):
        BaseLabel.__init__(self, text, 1, len(text) + 1, y, x)
