#########################################################
# Initial take on program flow. will be tested and
# modified once screens are made.
#
# We can discuss during our meeting on Sunday.
#
#########################################################

import curses
import atexit

class CDBCore:
    # Contains the main curses window
    stdscr = ""
  
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
        key = CDBCore.stdscr.getch()
        # TAB denotes move to next widget
        if key in [ord('\t'), 9]:
            CDBCore.CurrentScreen.NextWidget()
        # ENTER denotes move to next screen
        # TODO: Decide if this needs to be expanded for screens with
        #       multiple exit points, or if this will be handled within
        #       the screen itself
        elif key in [curses.KEY_ENTER, ord('\n'), 10]:
            CDBCore.History.append(CDBCore.CurrentScreen)
            CDBCore.CurrentScreen.Hide()
            CDBCore.CurrentScreen = CDBCore.CurrentScreen.Next()
            CDBCore.CurrentScreen.Show()
        # CTRL + TAB denotes go back to previous screen if there is one
        elif key in [1]: # TODO: identify CTRL+TAB key possibilities
            if len(CDBCore.History) > 0:
                CDBCore.CurrentScreen.Hide()
                CDBCore.CurrentScreen = CDBCore.History.pop()
                CDBCore.CurrentScreen.Show()
        else:
            # TODO: Popup to notify user before exitting application that an issue occured
            pass
    
    # Main method is the entry point of the application
    @staticmethod
    def Main():      
        # Prepare curses for use
        #InitCurses()
        
        # Show the home screen
        CDBCore.CurrentScreen.Show()
        
        # Process any further actions from the user
        while True:
            CDBCore.ProcessAction()
    
    # Cleans up curses on exit
    @staticmethod
    def CleanupCurses():
        try:
            curses.curs_set(0)
            curses.nocbreak()
            CDBCore.stdscr.keypad(0)
            curses.echo()
            curses.endwin()
        except:
            # TODO: add universal logging (especially for dev)
            pass # exit anyways
    
    # Initializes the curses library for use, and registers cleanup
    @staticmethod
    def InitCurses():
        # First register proper cleanup of curses
        atexit.register(CDBCore.CleanupCurses)
        
        # Next initialize curses for use
        CDBCore.stdscr = curses.initscr()
        try:
            # Not all terminals support hiding the cursor
            curses.curs_set(1)
        except:
            pass
        curses.cbreak()
        curses.noecho()
        CDBCore.stdscr.keypad(1)

