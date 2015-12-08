import sys
import curses
from BaseScreen import BaseScreen
from Button import BaseButton

class MainMenu(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self, screen_type="MainMenu")

    def Init(self):
        taskButton = BaseButton("Select Task", self.GoToTaskScreen, 3, 
                       len("Select Task") + 2, 1, 1, attr={"boxed": True, "y_offset" : 1, "x_offset" : 1})
        # OptButton = BaseButton("Options", testMethod, 3, len("Options") + 2, 1, 
        #                CWizButton.X + len(CWizButton) + 2, attr={"boxed": True, "y_offset" : 1, "x_offset" : 1})
        exitButton = BaseButton("Exit", sys.exit, 3, len("Exit") + 2, 1, 
                       taskButton.X + len(taskButton) + 2, attr={"boxed": True, "y_offset" : 1, "x_offset" : 1})

        self.ActionWidgets += [taskButton, exitButton]

    def GoToTaskScreen(self):
        from SelectTaskScreen import SelectTask
        from CDBCore import CDBCore

        taskScreen = SelectTask()
        CDBCore.ChangeCurrentScreen(taskScreen)