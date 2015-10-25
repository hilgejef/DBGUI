import curses
import curses.panel
from Label import Label

# 1. Text attribute includes "Press Enter To Dismiss"
# 2. Only dismissable by pressing Enter
# 3. Pads text with whitespace?
# Alternate - Tells screen to call Hide() on all other widget objects, then Show() on Enter Press?
""" PopUp """
class PopUp(Label):
    def __init__(self, text, y, x):
        text = text + "[ Press Enter To Dismiss ]"
        Label.__init__(self, text, y, x)
        
    def Active(self):
        selected = True
        # highlight current widget to show it is active
        self.Highlight()
        
        while selected:
            key = self.Win.getch()
            
            # Only capture Enter commands? Is this okay?
            if key in [curses.KEY_ENTER, ord('\n'), 10]:
            	# Add Hide() and Show() on other widgets?
                self.UnHighlight()
                self.Text = ""
                self.UpdateDisplay()
                selected = False

# # Is there a difference between No and Cancel?
# """ PopUpYesNoCancel """
# class PopUpYesNoCancel(Label):
#     pass