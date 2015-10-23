import curses
import curses.panel
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
                # TODO: give notification to screen object that TAB was pressed (for selecting next widget)
                #       potentially can use curses.ungetch(key) here