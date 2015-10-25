#########################################################
# Initial take on program flow. will be tested and
# modified once screens are made.
#
# We can discuss during our meeting on Sunday.
#
#########################################################

import curses

class Core:
    # TODO: set to base connection string object
    ConnectionString = ""
    
    # TODO: Set to home screen
    CurrentScreen = ""
    
    # TODO: Create menu screen
    MenuScreen = ""
    
    # TODO: Create status screen
    StatusScreen = ""
    
    # Stores the history of screens the user has visited
    History = []
    
    # Processes any actions from the user.  These actions are
    # passed through curses.ungetch(ch).
    @staticmethod
    def ProcessAction():
        key = curses.getch()
        # TAB denotes move to next widget
        if key in [ord('\t'), 9]:
            # TODO: move to next widget within the current screen
            self.CurrentScreen.NextWidget()
        # ENTER denotes move to next screen
        # TODO: Decide if this needs to be expanded for screens with
        #       multiple exit points, or if this will be handled within
        #       the screen itself
        elif key in [curses.KEY_ENTER, ord('\n'), 10]:
            self.History.append(self.CurrentScreen)
            self.CurrentScreen.Hide()
            self.CurrentScreen = self.CurrentScreen.Next()
            self.CurrentScreen.Show()
        # CTRL + TAB denotes go back to previous screen if there is one
        elif key in [1]: # TODO: identify CTRL+TAB key possibilities
            if len(self.History) > 0:
                self.CurrentScreen.Hide()
                self.CurrentScreen = self.History.pop()
                self.CurrentScreen.Show()
        else:
            # TODO: Popup to notify user before exitting application that an issue occured
            pass
    
    # Main method is the entry point of the application
    @staticmethod
    def Main():
        # Show the home screen
        self.CurrentScreen.Show()
        
        # Process any further actions from the user
        while True:
            ProcessAction()