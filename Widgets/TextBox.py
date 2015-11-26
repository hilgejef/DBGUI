import curses
import curses.panel
from BaseWidget import BaseWidget

""" TextBox """
class TextBox(BaseWidget):
    def __init__(self, height, width, y, x, attr=None, textbox_method=None):
        BaseWidget.__init__(self, height, width, y, x, attr)
        self.Text = ""
        self.DisplayText = ' ' * (width - 1)
        self.DisplayMode = "STANDARD"
        self.TextBoxMethod = textbox_method
        self.TextBoxDisplay()
        
    def Value(self):
        return self.Text
        
    def TextBoxDisplay(self):
        self.SetDisplayText()
        self.UpdateDisplay()

    def SetDisplayText(self):
        # self.DisplayMode settings:
        #        "STANDARD" - normal display for widget
        #        "TYPING" - display for widget while typing
        if self.DisplayMode == "STANDARD":
            self.DisplayText = self.Text[:(self.Characters - self.XPadding - 1)]
            if len(self.Text) >= self.Characters:
                self.DisplayText = self.DisplayText[:self.Characters - self.XPadding - 4] + "..."
        elif self.DisplayMode == "TYPING":
            self.DisplayText = self.Text[-(self.Characters - self.XPadding - 1):]
        else:
            print "Invalid display setting for TextBox Widget."
        
        if len(self.DisplayText) < (self.Characters - self.XPadding - 1):
            fill_in_with_blanks = ' ' * ((self.Characters - self.XPadding - 1) - len(self.DisplayText))
            self.DisplayText += fill_in_with_blanks
        
    def Active(self):        
        pass
            
        
    def ExecInput(self, key):
        # Special keys handled by CaptureText()
        #   ESC:       exits without capturing anything, current widget still highlighted
        #   ENTER:     exits with capturing all previously entered text, current widget still highlighted
        #   TAB:       exits with capturing and moves to next widget
        #   SHIFT-TAB: exits with capturing and moves to prev widget   NOTE! Shift+Tab does not appear to be capturable by ncurses
        #   BACKSPACE: removes last character from self.Text

        self.Win.move(0, min(len(self.Text), self.Characters - self.XPadding - 1))
        
        # ESC
        # 27 can mean either ALT or ESC in ncurses
        # following code from http://stackoverflow.com/questions/5977395/ncurses-and-esc-alt-keys
        # used to resolve ESC vs ALT+key with key input
        if key in [-1]:
            self.Text = old_text
            self.DisplayMode = "STANDARD"
            self.Highlight()
    
        # ENTER
        # - Additional option - can activate passed method on enter input
        elif key in [curses.KEY_ENTER, ord('\n'), 10]:
            self.DisplayMode = "STANDARD"
            self.Highlight()

            if self.TextBoxMethod:
                self.TextBoxMethod()
        
        # TAB
        elif key in [ord('\t'), 9]:
            self.DisplayMode = "STANDARD"

        # BACKSPACE
        elif key in [curses.KEY_BACKSPACE, ord('\b'), 10]:
            # erase last character entered
            self.Text = self.Text[:-1]
            self.DisplayMode = "TYPING"
        
        else:
            self.Text += chr(key)
            self.DisplayMode = "TYPING"
            
        self.TextBoxDisplay()