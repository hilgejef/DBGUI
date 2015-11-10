from BaseScreen import BaseScreen
from Label import BaseLabel
from Button import BaseButton

class HomeScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
        label = BaseLabel("Welcome to Database Explorer\n" +
        	              "-- Written By --\n" +
        	              "Richard Gagliano\n" +
        	              "Jon Moore\n" +
        	              "Jeffrey Hilger", 10, 10, 1, 1)
        BaseScreen.PassiveWidgets.append(label)