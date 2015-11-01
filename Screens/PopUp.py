import curses
import curses.panel
from BaseScreen import BaseScreen
from Label import Label
from Button import Button

# Base Class for PopUp
# PopUps are composed of 1 Label and 2/3 Button widgets
# Call PopUp with list values, i.e. [label] and [buttons]
""" PopUp """
class PopUp(BaseScreen):
    def __init__(self, label, buttons):
        BaseScreen.__init__(self)
        self.PassiveWidgets = label
        self.ActiveWidgets = buttons

# PopUpOkCancel = 1 Label and 2 Buttons
# Called with text string and 2 functions
# Functions are button methods (i.e. what happens when you activate them)
""" PopUpOkCancel """
class PopUpOkCancel(PopUp):
    def __init__(self, text, okMethod, cancelMethod):
        label = Label(text, 1, 1)
        okButton = Button("OK", okMethod, 10, 12)
        cancelButton = Button("Cancel", cancelMethod, 10, 2)
        PopUp.__init__(self, [label], [okButton, cancelButton])

# PopUpYesNoCancel = 1 Label and 3 Buttons
# Called with text string and 3 functions
""" PopUpYesNoCancel """
class PopUpYesNoCancel(PopUp):
    def __init__(self, text, yesMethod, noMethod, cancelMethod):
        label = Label(text, 1, 1)
        yesButton = Button("Yes", yesMethod, 10, 12)
        noButton = Button("No", noMethod, 10, 7)
        cancelButton = Button("Cancel", cancelMethod, 10, 2)
        PopUp.__init__(self, [label], [yesButton, noButton, cancelButton])    
        