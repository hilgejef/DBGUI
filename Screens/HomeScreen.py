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
        	              "Jeffrey Hilger", 13, 40, 5, 20, 
        	              attr={"boxed": True, "y_offset" : 4, "x_offset": 5, "text_y_center": True, "text_x_center" : True})
        self.PassiveWidgets.append(label)
        
        self.ActionWidgets.append(Button.Button(
            "Connect!",
            self.GoToNextScreen,
            CDBCore.CDBCore.MAIN_SCREEN_Y + 15,
            20,
            None,
            True
        ))
        
    def GoToNextScreen(self):
        curses.ungetch('\n');
        
    def Next(self):
        return self.NextScreen()
        