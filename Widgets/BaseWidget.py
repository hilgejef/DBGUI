import curses
import curses.panel

""" Base Widget """
class BaseWidget:

    # Default widget attributes
    default_attributes = {
        "boxed" : False,
        "vert_border" : False,
        "horiz_border" : False,
        "text_y_center" : False,
        "text_x_center" : False,
        "window_y_center" : False,
        "window_x_center" : False,
        "text_color" : 1,
        "bkgd_color" : 2,
        "y_offset" : 0,
        "x_offset" : 0,
        "text_mode" : curses.A_NORMAL,
        "use_display_text" : False
    }

    def __init__(self, height, width, y, x, attr=None):
        if attr == None:
            self.Init(height, width, y, x, BaseWidget.default_attributes)
        else:
            merged_attributes = BaseWidget.default_attributes.copy()
            merged_attributes.update(attr)
            self.Init(height, width, y, x, merged_attributes)

    def __len__(self):
        return self.Width

    def Init(self, height, width, y, x, attr):
        # Standard initializations
        self.Height = height
        self.Width = width
        self.Y = y
        self.X = x
        self.Win = curses.newwin(height, width, y, x)
        self.Pnl = curses.panel.new_panel(self.Win)

        # Text to override
        self.Text = ""
        self.DisplayText = ""

        # Attribute initializations
        self.TextMode = attr["text_mode"]
        self.Boxed = attr["boxed"]
        self.VertBorder = attr["vert_border"]
        self.HorizBorder = attr["horiz_border"]
        self.TextYCenter = attr["text_y_center"]
        self.TextXCenter = attr["text_x_center"]
        self.WindowYCenter = attr["window_y_center"]
        self.WindowXCenter = attr["window_x_center"]
        self.TextColor = curses.color_pair(attr["text_color"])
        self.BkgdColor = curses.color_pair(attr["bkgd_color"])
        self.YOffset = attr["y_offset"]
        self.XOffset = attr["x_offset"]
        self.UseDisplayText = attr["use_display_text"]

       # Determine padding attributes
        if self.HorizBorder or self.Boxed:
            self.XPadding = 2
        else:
            self.XPadding = 0

        # Legacy support
        self.Lines = height
        self.Characters = width
    
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

        elif self.VertBorder:
            self.Win.border(" ", " ", 0, 0, " ", " ", " ", " ")

        elif self.HorizBorder:
            self.Win.border(0, 0, " ", " ", " ", " ", " ", " ")

        self.Win.bkgd(' ', self.BkgdColor)

        if self.TextYCenter:
            num_lines = self.Text.count('\n')
            YOffset = (self.Height - num_lines) / 2
        else:
            YOffset = self.YOffset

        if self.UseDisplayText:
            text = self.DisplayText
        else:
            text = self.Text

        if self.TextXCenter:
            for line, substr in enumerate(text.split('\n')):
                XOffset = (self.Width - len(substr)) / 2 
                self.Win.addnstr(YOffset + line, XOffset, substr, 
                                 self.Width  - XOffset - 1, self.TextMode | self.TextColor)
        else:
            for line, substr in enumerate(text.split('\n')):
                self.Win.addnstr(YOffset + line, self.XOffset, substr,
                                 self.Width - self.XOffset - 1, self.TextMode | self.TextColor)
            
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

    # Base input handler - accepts input and calls ExecBase() and ExecInput()
    def HandleInput(self, inp):
        self.ExecBase(inp)
        self.ExecInput(inp)

    # Base function to implement input actions common to all widgets
    def ExecBase(self, inp):
        if inp in [ord('\t'), 9]:
            self.UnHighlight()

        else:
            pass

    # Overloaded by specific widget
    def ExecInput(self, inp):
        pass
    
    # Virtual Active() function so that active can be used
    # across all widgets
    def Active(self):
        pass