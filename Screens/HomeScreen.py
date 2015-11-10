from BaseScreen import BaseScreen
from Label import BaseLabel
from Button import BaseButton

class HomeScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)

    def Init(self):
        label = BaseLabel("Welcome to Database Explorer\n" +
        	              "-- Written By --\n" +
        	              "Richard Gagliano\n" +
        	              "Jon Moore\n" +
        	              "Jeffrey Hilger", 13, 40, 5, 20, boxed=True, y_offset=4, x_offset=5)
        self.PassiveWidgets.append(label)