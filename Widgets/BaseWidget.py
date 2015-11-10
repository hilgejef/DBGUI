import curses
import curses.panel

""" Base Widget """
class BaseWidget:
    def __init__(self, height, width, y, x, boxed=False, center=False, text_color=1, bkgd_color=2,
                 y_offset=0, x_offset=0):
        self.height = height
        self.width = width
        self.Lines = height
        self.Characters = width
        self.Y = y
        self.X = x
        self.Win = curses.newwin(height, width, y, x)
        self.Pnl = curses.panel.new_panel(self.Win)
        self.Text = ""
        self.Boxed = boxed
        self.Centered = center
        self.TextMode = curses.A_NORMAL
        self.TextColor = curses.color_pair(text_color)
        self.BkgdColor = curses.color_pair(bkgd_color)
        self.YOffset = y_offset
        self.XOffset = x_offset

    def __len__(self):
        if self.Boxed:
            return len(self.Text) + 2
        else:
            return len(self.Text)
    
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
            self.Win.box()
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
    
    # Updates the display with the current text mode
    def UpdateDisplay(self):
        self.Win.erase()

        if self.Boxed:
            self.Win.box()

        self.Win.bkgd(' ', self.BkgdColor)

        if self.Centered:
            pass
            # TODO: Add centering for text

        else:
            for line, substr in enumerate(self.Text.split('\n')):
                self.Win.addstr(self.YOffset + line, self.XOffset, 
                                substr, self.TextMode | self.TextColor)
            
        self.Refresh()

    # Highlights the text by reversing the foreground/background
    def Highlight(self):
        self.TextMode = curses.A_REVERSE
        self.UpdateDisplay()
    
    # UnHighlights the text by setting foreground/background to current
    # terminal colors
    def UnHighlight(self):
        self.TextMode = curses.A_NORMAL
        self.UpdateDisplay()
    
    # Virtual Active() function so that active can be used
    # across all widgets
    def Active(self):
        pass