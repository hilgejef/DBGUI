#########################################################
# Label
#
# Presents text to the user.
#
#########################################################

import curses
import curses.panel
from BaseWidget import BaseWidget

""" BaseLabel """
class BaseLabel(BaseWidget):
	def __init__(self, text, height, width, y, x, attr=None):
		BaseWidget.__init__(self, height, width, y, x, attr)
		self.Text = text
		self.Type = "Label"
		self.UpdateDisplay()

""" Label """
class Label(BaseLabel):
    def __init__(self, text, y, x, attr=None):
        BaseLabel.__init__(self, text, 1, len(text) + 1, y, x, attr)
