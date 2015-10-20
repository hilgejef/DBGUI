import curses
import curses.panel

""" Base Widget """
class BaseWidget:
    def __init__(self, lines, characters, y, x):
        self.Lines = lines
        self.Characters = characters
        self.Y = y
        self.X = x
        self.Win = curses.newwin(lines, characters, y, x)
        self.Pnl = curses.panel.new_panel(self.Win)
    
    def Refresh(self):
        try:
            curses.panel.update_panels()
            curses.doupdate()
        except:
            # TODO: Replace with global status screen output
            print "Could not refresh."
    
    def Hide(self):
        try:
            self.Pnl.hide()
        except:
            # TODO: Replace with global status screen output
            print "Could not hide panel."
        
    def Show(self):
        try:
            self.Pnl.show()
        except:
            # TODO: Replace with global status screen output
            print "Could not show panel."
    
    def BordersOn(self):
        try:
            # TODO: Decide on border rules
            pass
        except:
            # TODO: Replace with global status screen output
            print "Could not draw borders."
    
    def BordersOff(self):
        try:
            # TODO: decide on border rules
            pass
        except:
            # TODO: Replace with global status screen output
            print "Could not remove borders."
    
    def Move(self, y, x):
        try:
            self.Pnl.move(y, x)
        except:
            # TODO: Replace with global status screen output
            print "Could not move panel."

    def ToTop(self):
        try:
            self.Pnl.top()
        except:
            # TODO: Replace with global status screen output
            print "Could not move panel to top of the stack."
    
    def ToBottom(self):
        try:
            self.Pnl.bottom()
        except:
            # TODO: Replace with global status screen output
            print "Could not move panel to bottom of the stack."
