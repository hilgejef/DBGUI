import curses
import curses.panel
from BaseWidget import BaseWidget

""" Base CheckBox """
class BaseCheckBox(BaseWidget):
    def __init__(self, checked_text, unchecked_text,
                 height, width, y, x, attr=None):
        BaseWidget.__init__(self, height, width, y, x, attr)
        self.CheckedText = "< " + checked_text + " >"
        self.UncheckedText = "< " + unchecked_text + " >"
        self.Text = self.UncheckedText
        self.Checked = False
        self.UpdateDisplay()
  
    def Value(self):
        return self.Checked
        
    def Check(self):
        self.Checked = not self.Checked
        if self.Checked:
            self.Text = self.CheckedText
        else:
            self.Text = self.UncheckedText
        
        self.UpdateDisplay()
        
    def Active(self):
        selected = True
        # highlight current widget to show it is active
        self.Highlight()
        
        while selected:
            key = self.Win.getch()
            
            # capture ENTER, TAB, and BACKTAB keystrokes
            if key in [curses.KEY_ENTER, ord('\n'), 10]:
                self.Check()

            elif key in [ord('\t'), 9]:
                # stop highlighting current widget
                self.UnHighlight()
                selected = False
                curses.ungetch(key)
                
            # go to menu (SHIFT-M or F1)
            # or go to status screen (SHIFT-M or F8)
            elif key in [curses.KEY_F1, 77, curses.KEY_F8, 76]:
                selected = False
                curses.ungetch(key)

""" Check Box """
class CheckBox(BaseCheckBox):
    def __init__(self, checked_text, unchecked_text, y, x):
        height = 1
        width = max(len(checked_text), len(unchecked_text)) + 5
        BaseCheckBox.__init__(self, checked_text, unchecked_text, height, width, y, x)
        