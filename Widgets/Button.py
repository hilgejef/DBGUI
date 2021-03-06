#########################################################
# Button
#
# Executes actions when <ENTER> is pressed.
#
#########################################################

import curses
import curses.panel
from Label import BaseLabel

""" BaseButton """
class BaseButton(BaseLabel):
    def __init__(self, text, method, height, width, y, x, attr=None):
        BaseLabel.__init__(self, text, height, width, y, x, attr)
        self.CallMethod = method
        self.Type = "Button"
        
    # This widget now has the focus.  Read the user input,
    # and decide what to do next.
    def Active(self):
        selected = True
        # highlight current widget to show it is active
        self.Highlight()
        
        while selected:
            key = self.Win.getch()
            
            # capture ENTER, TAB, and BACKTAB keystrokes
            if key in [curses.KEY_ENTER, ord('\n'), 10]:
                self.UnHighlight()
                selected = False
                self.CallMethod()
            
            elif key in [ord('\t'), 9] and not self.DisableTab:
                # stop highlighting current widget
                self.UnHighlight()
                selected = False
                curses.ungetch(key)     # pass tab along so Screen will know to go to next widget

            # go to menu (SHIFT-M or F1)
            # or go to status screen (SHIFT-M or F8)
            elif key in [curses.KEY_F1, 77, curses.KEY_F8, 76] and not self.DisableScreenSwitch:
                selected = False
                curses.ungetch(key)

""" Button """
class Button(BaseButton):
    def __init__(self, text, method, y, x, attr=None, no_brackets=False):
        if not no_brackets:
            text = "[ " + text + " ]"
        BaseButton.__init__(self, text, method, 1, len(text) + 1, y, x, attr)