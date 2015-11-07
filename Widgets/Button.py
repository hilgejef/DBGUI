import curses
import curses.panel
from Label import BaseLabel

""" BaseButton """
class BaseButton(BaseLabel):
    def __init__(self, text, method, l, c, y, x):
        text = "[ " + text + " ]"
        BaseLabel.__init__(self, text, l, c, y, x)
        self.CallMethod = method
        
    def Active(self):
        selected = True
        # highlight current widget to show it is active
        self.Highlight()
        
        while selected:
            key = self.Win.getch()
            
            # capture ENTER, TAB, and BACKTAB keystrokes
            if key in [curses.KEY_ENTER, ord('\n'), 10]:
                # should I leave the deselecting of the widget for the screen handler object?
                #   - I think this should be handled here so that the behavior will be consistent
                #     accross the application. Can't think of a good reason not to do it here. - Rich
                self.UnHighlight()
                selected = False
                self.CallMethod()
            
            elif key in [ord('\t'), 9]:
                # stop highlighting current widget
                self.UnHighlight()
                selected = False
                curses.ungetch('\t') # Notify the core that tab was pressed


""" Button """
class Button(BaseButton):
    def __init__(self, text, method, y, x):
        BaseButton.__init__(self, text, method, 1, len(text) + 1, y, x)