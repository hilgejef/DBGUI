import curses
import curses.panel
from Label import BaseLabel

""" BaseButton """
class BaseButton(BaseLabel):
    def __init__(self, text, method, height, width, y, x, attr=None):
        BaseLabel.__init__(self, text, height, width, y, x, attr)
        self.CallMethod = method
        
    # -- IMO, should be rewritten to be handled in Core, and
    # keys passed to widget, which will have a key handler
    def Active(self):
        self.Highlight()

    def ExecInput(self, inp):
        if inp in [curses.KEY_ENTER, ord('\n'), 10]:
            self.CallMethod()
            
        elif inp in [ord('\t'), 9]:
            self.UnHighlight()

        else:
            pass

""" Button """
class Button(BaseButton):
    def __init__(self, text, method, y, x, attr=None, no_brackets=False):
        if not no_brackets:
            text = "[ " + text + " ]"
        BaseButton.__init__(self, text, method, 1, len(text) + 1, y, x, attr)