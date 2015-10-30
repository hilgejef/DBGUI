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
        BaseScreen.__init__()
        self.PassiveWidgets = label
        self.ActiveWidgets = buttons
        self.Show()

# PopUpOkCancel = 1 Label and 2 Buttons
# Called with text string and 2 functions
# Functions are button methods (i.e. what happens when you activate them)
""" PopUpOkCancel """
class PopUpOkCancel(PopUp):
    def __init__(self, text, okMethod, cancelMethod):
        label = Label(text, 1, 1)
        okButton = Button("OK", okMethod, 14, 1)
        cancelButton = Button("Cancel", cancelMethod, 1, 1)
        PopUp.__init__([label], [okButton, cancelButton])

# PopUpYesNoCancel = 1 Label and 3 Buttons
# Called with text string and 3 functions
""" PopUpYesNoCancel """
class PopUpYesNoCancel(PopUp):
    def __init__(self, text, yesMethod, noMethod, cancelMethod):
        label = Label(text, 1, 1)
        yesButton = Button("Yes", yesMethod, 14, 1)
        noButton = Button("No", noMethod, 7, 1)
        cancelButton = Button("Cancel", cancelMethod, 1, 1)
        PopUp.__init__([label], [yesButton, noButton, cancelButton])    
        