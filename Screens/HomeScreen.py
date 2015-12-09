import CDBCore
import Button
import curses
from BaseScreen import BaseScreen
from Label import BaseLabel
import ConnectionWizard

class HomeScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self, screen_type="HomeScreen")

    def Init(self):
        self.NextScreen = ConnectionWizard.ConnectionWizard
        label = BaseLabel("Welcome to Database Explorer\n" +
        	              "-- Written By --\n" +
        	              "Richard Gagliano\n" +
        	              "Jon Moore\n" +
        	              "Jeffrey Hilger", 9, 40, 5, 20, 
        	              attr={"boxed": True, "y_offset" : 1, "x_offset": 5, "text_y_center": True, "text_x_center" : True})
        self.PassiveWidgets.append(label)
        
        self.ActionWidgets.append(Button.BaseButton(
            "Connect!",
            self.GoToNextScreen,
            3,
            len("Connect!") + 2,
            CDBCore.CDBCore.MAIN_SCREEN_Y + 12,
            50,
            attr={"boxed" : True, "y_offset" : 1, "x_offset" : 1}
        ))

    def GoToNextScreen(self):
        curses.ungetch('\n');
        
    def Next(self):
        return self.NextScreen()
        