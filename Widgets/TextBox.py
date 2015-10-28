import curses
import curses.panel
from BaseWidget import BaseWidget

""" Text Box """
class TextBox(BaseWidget):
    def __init__(self, height, width, y, x):
        BaseWidget.__init__(self, height, width, y, x)
        self.Text = ""
        self.DisplayText = " " * (self.Characters - 1)
        self.DisplayMode = "STANDARD"
        self.TextMode = curses.A_NORMAL
        self.Refresh()
        
    def Value(self):
        return self.Text
        
    # Overwrite BaseWidget method
    def UpdateDisplay(self):
        self.Win.erase()
        self.SetDisplayText()
        self.Win.addstr(self.DisplayText, self.TextMode)
        self.Refresh()
        
    def SetDisplayText(self):
        # self.DisplayMode settings:
        #        "STANDARD" - normal display for widget
        #        "TYPING" - display for widget while typing
        if self.DisplayMode == "STANDARD":
            self.DisplayText = self.Text[:(self.Characters - 1)]
            if len(self.Text) >= self.Characters:
                self.DisplayText = self.DisplayText[:self.Characters-4] + "..."
        elif self.DisplayMode == "TYPING":
            self.DisplayText = self.Text[-(self.Characters - 1):]
        else:
            print "Invalid display setting for TextBox Widget."
        
        if len(self.DisplayText) < (self.Characters - 1):
            fill_in_with_blanks = " " * (len(self.DisplayText) - (self.Characters - 1))
            self.DisplayText = self.DisplayText + fill_in_with_blanks
        
    def Active(self):        
        # Special keys handled by Active()
        #   ENTER:     enters into capture text mode
        #   TAB:       exits with capturing and moves to next widget
        
        self.Win.move(0,0)
        capturing = True
        
        while capturing:
            self.Win.move(0,0)
            key = self.Win.getch()
            
            # ENTER
            if key in [curses.KEY_ENTER, ord('\n'), 10]:
                self.CaptureText()
            
            # TAB
            elif key in [ord('\t'), 9]:
                curses.ungetch('\t') # Notify the core that tab was pressed
                capturing = False
            
        
    def CaptureText(self):
        # Special keys handled by CaptureText()
        #   ESC:       exits without capturing anything, current widget still highlighted
        #   ENTER:     exits with capturing all previously entered text, current widget still highlighted
        #   TAB:       exits with capturing and moves to next widget
        #   SHIFT-TAB: exits with capturing and moves to prev widget   NOTE! Shift+Tab does not appear to be capturable by ncurses
        #   BACKSPACE: removes last character from self.Text
        
        
        capturing = True
        old_text = self.Text
        self.Highlight()
        self.UpdateDisplay()
        
        while capturing:
            key = self.Win.getch()
            
            # in case no delay mode is set to true
            if key == -1:
                pass
            
            # ESC
            # 27 can mean either ALT or ESC in ncurses
            # following code from http://stackoverflow.com/questions/5977395/ncurses-and-esc-alt-keys
            # used to resolve ESC vs ALT+key with key input
            if key == 27:
                self.Win.nodelay(True)
                n = self.Win.getch()
                if n == -1:
                    # ESC was pressed and not ALT
                    self.Text = old_text
                    self.UnHighlight()
                    self.DisplayMode = "STANDARD"
                    capturing = False
                self.Win.nodelay(False)
        
            # ENTER
            elif key in [curses.KEY_ENTER, ord('\n'), 10]:
                self.UnHighlight()
                self.DisplayMode = "STANDARD"
                capturing = False
            
            # TAB
            elif key in [ord('\t'), 9]:
                self.UnHighlight()
                self.DisplayMode = "STANDARD"
                capturing = False
                curses.ungetch('\t') # Notify the core that tab was pressed
            
            # SHIFT+TAB
            
            # TODO: it does not appear to be possible to capture shift+tab in curses
            
                # TODO: give notification to screen object that SHIFT+TAB was pressed (for selecting next widget)
                #       potentially can use curses.ungetch(key) here
            
            # BACKSPACE
            elif key in [curses.KEY_BACKSPACE, ord('\b'), 10]:
                # erase last character entered
                self.Text = self.Text[:-1]
                self.DisplayMode = "TYPING"
            
            else:
                self.Text += chr(key)
                self.DisplayMode = "TYPING"
                
            self.UpdateDisplay()
            
        