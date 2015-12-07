import curses
import curses.panel
from Label import BaseLabel

""" BaseButton """
class BaseButton(BaseLabel):
    def __init__(self, text, method, height, width, y, x, attr=None):
        BaseLabel.__init__(self, text, height, width, y, x, attr)
        self.CallMethod = method
        self.Type = "Button"
        
    # -- IMO, should be rewritten to be handled in Core, and
    # keys passed to widget, which will have a key handler
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
                curses.ungetch(key)     # pass tab along so Screen will know to go to next widget

            # go to menu (SHIFT-M or F1)
            elif key in [curses.KEY_F1, 77]:
                selected = False
                curses.ungetch(key)
            # Temporary - deselection by any key other than Tab/Enter
            #else:
            #    selected = False

""" Button """
class Button(BaseButton):
    def __init__(self, text, method, y, x, attr=None, no_brackets=False):
        if not no_brackets:
            text = "[ " + text + " ]"
        BaseButton.__init__(self, text, method, 1, len(text) + 1, y, x, attr)