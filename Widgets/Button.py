import curses
import curses.panel
#from BaseWidget import BaseWidget
from Label import Label

""" Button """
class Button(Label):
    def __init__(self, text, method, y, x):
        text = "[ " + text + " ]"
        Label.__init__(self, text, y, x)
        self.CallMethod = method
        
    def Active(self):
        selected = True
        # highlight current widget to show it is active
        self.Highlight()
        
        while selected:
            key = self.Win.getch()
            
            # capture ENTER, TAB, and BACKTAB keystrokes
            if key in [curses.KEY_ENTER, ord('\n'), 10]:
                self.CallMethod()
                
                # should I leave the deselecting of the widget for the screen handler object?
                self.UnHighlight()
                selected = False

            elif key in [ord('\t'), 9]:
                # stop highlighting current widget
                self.UnHighlight()
                selected = False
                # TODO: give notification to screen object that TAB was pressed (for selecting next widget)
                #       potentially can use curses.ungetch(key) here