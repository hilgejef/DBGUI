import curses
import curses.panel
import CDBCore
from BaseScreen import BaseScreen
from Label import BaseLabel
from Button import BaseButton
from BaseWidget import BaseWidget

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
        cancelButton = BaseButton("Cancel", cancelMethod, 3, 8, 10, 13, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        PopUp.__init__(self, [label], [okButton, cancelButton])

# PopUpYesNoCancel = 1 Label and 3 Buttons
# Called with text string and 3 functions
""" PopUpYesNoCancel """
class PopUpYesNoCancel(PopUp):
    def __init__(self, text, yesMethod, noMethod, cancelMethod):
        label = BaseLabel(text, 3, 20, 5, 5, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        yesButton = BaseButton("Yes", yesMethod, 3, 5, 10, 5, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        noButton = BaseButton("No", noMethod, 3, 4, 10, 11, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        cancelButton = BaseButton("Cancel", cancelMethod, 3, 8, 10, 17, {"boxed":True, "x_offset" : 1, "y_offset" : 1})
        PopUp.__init__(self, [label], [yesButton, noButton, cancelButton])    
    
# PopUpOk = 1 Label and 1 Buttons
# Called with text string and 1 functions
# Function is button method (i.e. what happens when you activate them, typically just to close screen)
""" PopUpOkCancel """
class PopUpOk(PopUp):
    def __init__(self, text):
        screenBorder = BaseWidget(12, 50, 5, 15)
        screenBorder.Win.border('|', '|', '-', '-', '+', '+', '+', '+')
        label = BaseLabel(text, 7, 48, 6, 16)
        okButton = BaseButton("OK", self.ClosePopUp, 1, 4, 13, 36, {"disable_screen_switch":True})
        PopUp.__init__(self, [screenBorder, label], [okButton])
        
    def ClosePopUp(self):
        self.Hide()
        CDBCore.PopUp = None