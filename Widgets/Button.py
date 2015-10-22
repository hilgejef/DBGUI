import curses
import curses.panel
from BaseWidget import BaseWidget

""" Button """
class Button(BaseWidget):
    def __init__(self, text, method, y, x):
        BaseWidget.__init__(self, 1, len(text) + 5, y, x)
        self.Text = "[ " + text + " ]"
        self.CallMethod = method
        self.TextMode = curses.A_NORMAL
        self.Refresh()
        
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
                self.CallMethod()
                
                # should I leave the deselecting of the widget for the screen handler object?
                self.TextMode = curses.A_NORMAL
                self.DisplayText()
                selected = False

            elif key in [ord('\t'), 9]:
                # stop highlighting current widget
                self.TextMode = curses.A_NORMAL
                self.DisplayText()
                selected = False
                # TODO: give notification to screen object that TAB was pressed (for selecting next widget)
                #       potentially can use curses.ungetch(key) here