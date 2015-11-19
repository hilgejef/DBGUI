import curses
import curses.panel
from BaseScreen import BaseScreen
from Label import BaseLabel
from Button import BaseButton

# Base Class for PopUp
# PopUps are composed of 1 Label and 2/3 Button widgets
# Call PopUp with list values, i.e. [label] and [buttons]
""" PopUp """
class PopUp(BaseScreen):
    def __init__(self, label, buttons):
        BaseScreen.__init__(self)
        self.PassiveWidgets = label
        self.ActionWidgets = buttons

# PopUpOkCancel = 1 Label and 2 Buttons
# Called with text string and 2 functions
# Functions are button methods (i.e. what happens when you activate them)
""" PopUpOkCancel """
class PopUpOkCancel(PopUp):
    def __init__(self, text, okMethod, cancelMethod):
        label = BaseLabel(text, 3, 20, 5, 5, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        okButton = BaseButton("OK", okMethod, 3, 4, 10, 5, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        cancelButton = BaseButton("Cancel", cancelMethod, 3, 7, 10, 11, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        PopUp.__init__(self, [label], [okButton, cancelButton])

# PopUpYesNoCancel = 1 Label and 3 Buttons
# Called with text string and 3 functions
""" PopUpYesNoCancel """
class PopUpYesNoCancel(PopUp):
    def __init__(self, text, yesMethod, noMethod, cancelMethod):
        label = BaseLabel(text, 3, 20, 5, 5, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        yesButton = BaseButton("Yes", yesMethod, 3, 5, 10, 5, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        yesButton = BaseButton("No", noMethod, 3, 4, 10, 11, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        cancelButton = BaseButton("Cancel", cancelMethod, 3, 7, 10, 15, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        PopUp.__init__(self, [label], [yesButton, noButton, cancelButton])    
        