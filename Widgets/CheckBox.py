import curses
import curses.panel
from BaseWidget import BaseWidget

""" Check Box """
class CheckBox(BaseWidget):
    def __init__(self, checked_text, unchecked_text, y, x):
        height = 1
        width = max(len(checked_text), len(unchecked_text)) + 5
        BaseWidget.__init__(self, height, width, y, x)
        self.CheckedText = "< " + checked_text + " >"
        self.UncheckedText = "< " + unchecked_text + " >"
        self.Text = self.UncheckedText
        self.TextMode = curses.A_NORMAL
        self.Checked = False
        self.Win.addstr(0, 0, self.Text, self.TextMode)
        self.Refresh()
        
    def Value(self):
        return self.Checked
        
    def Check(self):
        self.Checked = not self.Checked
        if self.Checked:
            self.Text = self.CheckedText
        else:
            self.Text = self.UncheckedText
        
        self.DisplayText()
        
    def DisplayText(self):
        self.Win.addstr(0, 0, " " * (self.Characters - 1))
        self.Win.addstr(0, 0, self.Text, self.TextMode)
        self.Refresh()
        
    def Active(self):
        selected = True
        # highlight current widget to show it is active
        self.TextMode = curses.A_REVERSE
        self.DisplayText()
        self.Refresh()
        
        while selected:
            key = self.Win.getch()
            
            # capture ENTER, TAB, and BACKTAB keystrokes
            if key in [curses.KEY_ENTER, ord('\n'), 10]:
                self.Check()
                capturing = False

            elif key in [ord('\t'), 9]:
                # stop highlighting current widget
                self.TextMode = curses.A_NORMAL
                self.DisplayText()
                selected = False
                # TODO: give notification to screen object that TAB was pressed (for selecting next widget)
                #       potentially can use curses.ungetch(key) here
    
    
            
        