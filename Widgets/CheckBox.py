import curses
import curses.panel
from BaseWidget import BaseWidget

""" Check Box """
class CheckBox(BaseWidget):
    def __init__(self, checked_text, unchecked_text, y, x):
        height = 1
        width = max(len(checked_text), len(unchecked_text)) + 4
        BaseWidget.__init__(self, height, width, y, x)
        self.CheckedText = "< " + checked_text + " >"
        self.UncheckedText = "< " + unchecked_text + " >"
        self.TextMode = curses.A_NORMAL
        self.Checked = False
        self.Win.addstr(self.UncheckedText, self.TextMode)
        self.Refresh()
        
    def Value(self):
        return self.Checked
        
    def Check(self):
        self.Checked = not self.Checked
        if self.Checked:
            displayText = self.CheckedText
        else:
            displayText = self.UncheckedText
        
        self.Win.addstr(" " * self.Characters)
        self.Win.addstr(displayText, self.TextMode)
        self.Refresh()
        
    def Active(self):
        selected = True
        self.TextMode = curses.A_REVERSE
        
        while selected:
            key = self.Win.getch()
            
            # capture ENTER, TAB, and BACKTAB keystrokes
            if key in [curses.KEY_ENTER, ord('\n'), 10]:
                self.Check()
                capturing = False

            elif key in [ord('\t'), 9]:
                self.TextMode = curses.A_NORMAL
                selected = False
                # TODO: give notification to screen object that TAB was pressed (for selecting next widget)
                #       potentially can use curses.ungetch(key) here
    
    
            
        