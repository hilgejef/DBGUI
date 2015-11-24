import sys
from BaseScreen import BaseScreen
from Button import BaseButton

def testMethod():
	pass

class MainMenu(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self, screen_type="MainMenu")

    def Init(self):
        CWizButton = BaseButton("Connection Wizard", testMethod, 3, 
        	           len("Connection Wizard") + 2, 1, 1, attr={"boxed": True, "y_offset" : 1, "x_offset" : 1})
        OptButton = BaseButton("Options", testMethod, 3, len("Options") + 2, 1, 
        	           CWizButton.X + len(CWizButton) + 2, attr={"boxed": True, "y_offset" : 1, "x_offset" : 1})
        ExitButton = BaseButton("Exit", sys.exit, 3, len("Exit") + 2, 1, 
        	           OptButton.X + len(OptButton) + 2, attr={"boxed": True, "y_offset" : 1, "x_offset" : 1})

        self.ActionWidgets += [CWizButton, OptButton, ExitButton]