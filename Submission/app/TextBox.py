#########################################################
# TextBox
#
# Allows the user to modify text when <ENTER> is pressed.
#
#########################################################

import curses
import curses.panel
from BaseWidget import BaseWidget

""" Text Box """
class TextBox(BaseWidget):
    def __init__(self, height, width, y, x):
        BaseWidget.__init__(self, height, width, y, x)
        self.Text = ""
        self.DisplayText = ' ' * (width - 1)
        self.DisplayMode = "STANDARD"
        self.UpdateDisplay()
        
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
            fill_in_with_blanks = ' ' * ((self.Characters - 1) - len(self.DisplayText))
            self.DisplayText += fill_in_with_blanks
        
    def Active(self):        
        # Special keys handled by Active()
        #   ENTER:     enters into capture text mode
        #   TAB:       exits with capturing and moves to next widget
        
        self.Highlight()
        capturing = True
        
        while capturing:
            #self.Win.move(0,0)
            key = self.Win.getch()
            
            # ENTER
            if key in [curses.KEY_ENTER, ord('\n'), 10]:
                self.CaptureText()
            
            # TAB
            elif key in [ord('\t'), 9]:
                self.UnHighlight()
                curses.ungetch('\t') # Notify the core that tab was pressed
                capturing = False
            
            # go to menu (SHIFT-M or F1)
            # or go to status screen (SHIFT-M or F8)
            elif key in [curses.KEY_F1, 77, curses.KEY_F8, 76] and not self.DisableScreenSwitch:
                capturing = False
                curses.ungetch(key)
            
        
    def CaptureText(self):
        # Special keys handled by CaptureText()
        #   ESC:       exits without capturing anything, current widget still highlighted
        #   ENTER:     exits with capturing all previously entered text, current widget still highlighted
        #   TAB:       exits with capturing and moves to next widget
        #   BACKSPACE: removes last character from self.Text
        
        capturing = True
        old_text = self.Text
        self.UnHighlight()
        
        while capturing:
            self.Win.move(0, min(len(self.Text), self.Characters - 1))
            
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
                    self.DisplayMode = "STANDARD"
                    self.Highlight()
                    capturing = False
                self.Win.nodelay(False)
        
            # ENTER
            elif key in [curses.KEY_ENTER, ord('\n'), 10]:
                self.DisplayMode = "STANDARD"
                self.Highlight()
                capturing = False
            
            # TAB
            elif key in [ord('\t'), 9]:
                self.DisplayMode = "STANDARD"
                self.UnHighlight()
                capturing = False
                curses.ungetch('\t') # Notify the core that tab was pressed
            
            # -- Added 8 and 127, additional possible backspace inputs (127 on my system)
            # http://stackoverflow.com/questions/4363309/how-to-check-for-the-backspace-character-in-c
            elif key in [curses.KEY_BACKSPACE, ord('\b'), 10, 8, 127]:
                # erase last character entered
                self.Text = self.Text[:-1]
                self.DisplayMode = "TYPING"
            
            else:
                self.Text += chr(key)
                self.DisplayMode = "TYPING"
                
            self.UpdateDisplay()

# ----------------------------------------------------------------

# Modified TextBox for use in AlterTables
# Uses BaseWidget display and has modified active method
""" ModTextBox """
class ModTextBox(BaseWidget):
    def __init__(self, height, width, y, x, attr=None):
        BaseWidget.__init__(self, height, width, y, x, attr)
        self.Type = "TextBox"
        self.Text = ""
        self.DisplayText = ' ' * (width - 1)
        self.DisplayMode = "STANDARD"
        self.IsActive = False
        self.UpdateDisplay()
        
    def Value(self):
        return self.Text
        
    # Overwrite BaseWidget method
    def UpdateDisplay(self):
        self.SetDisplayText()
        BaseWidget.UpdateDisplay(self, useDisplay=True)

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
            fill_in_with_blanks = ' ' * ((self.Characters - 1) - len(self.DisplayText))
            self.DisplayText += fill_in_with_blanks
        
    def Active(self):        
        # Special keys handled by Active()
        #   ENTER:     enters into capture text mode
        #   TAB:       exits with capturing and moves to next widget
        
        self.CaptureText()
        
    def CaptureText(self):
        # Special keys handled by CaptureText()
        #   ESC:       exits without capturing anything, current widget still highlighted
        #   ENTER:     exits with capturing all previously entered text, current widget still highlighted
        #   TAB:       exits with capturing and moves to next widget
        #   BACKSPACE: removes last character from self.Text
        
        capturing = True
        old_text = self.Text
        self.UnHighlight()
        
        while capturing:
            self.Win.move(self.YOffset, min(len(self.Text) + self.XOffset, self.Characters - 1))
            
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
                    self.DisplayMode = "STANDARD"
                    self.Highlight()
                    capturing = False
                self.Win.nodelay(False)
        
            # ENTER
            elif key in [curses.KEY_ENTER, ord('\n'), 10]:
                self.DisplayMode = "STANDARD"
                self.Highlight()
                capturing = False
                curses.ungetch('\n')
            
            # TAB
            elif key in [ord('\t'), 9]:
                self.DisplayMode = "STANDARD"
                self.UnHighlight()
                capturing = False
                curses.ungetch('\t')

            # BACKSPACE
            # -- Added 8 and 127, additional possible backspace inputs (127 on my system)
            # http://stackoverflow.com/questions/4363309/how-to-check-for-the-backspace-character-in-c
            elif key in [curses.KEY_BACKSPACE, ord('\b'), 10, 8, 127]:
                # erase last character entered
                self.Text = self.Text[:-1]
                self.DisplayMode = "TYPING"
            
            else:
                if len(chr(key)) > 1:
                    pass
                else:
                    self.Text += chr(key)
                    self.DisplayMode = "TYPING"
                
            self.UpdateDisplay()

