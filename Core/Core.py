#########################################################
# Initial take on program flow. will be tested and
# modified once screens are made.
#
# We can discuss during our meeting on Sunday.
#
#########################################################

import curses
import atexit

class Core:
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
        key = Core.stdscr.getch()
        # TAB denotes move to next widget
        if key in [ord('\t'), 9]:
            Core.CurrentScreen.NextWidget()
        # ENTER denotes move to next screen
        # TODO: Decide if this needs to be expanded for screens with
        #       multiple exit points, or if this will be handled within
        #       the screen itself
        elif key in [curses.KEY_ENTER, ord('\n'), 10]:
            Core.History.append(Core.CurrentScreen)
            Core.CurrentScreen.Hide()
            Core.CurrentScreen = Core.CurrentScreen.Next()
            Core.CurrentScreen.Show()
        # CTRL + TAB denotes go back to previous screen if there is one
        elif key in [1]: # TODO: identify CTRL+TAB key possibilities
            if len(Core.History) > 0:
                Core.CurrentScreen.Hide()
                Core.CurrentScreen = Core.History.pop()
                Core.CurrentScreen.Show()
        else:
            # TODO: Popup to notify user before exitting application that an issue occured
            pass
    
    # Main method is the entry point of the application
    @staticmethod
    def Main():      
        # Prepare curses for use
        #InitCurses()
        
        # Show the home screen
        Core.CurrentScreen.Show()
        
        # Process any further actions from the user
        while True:
            Core.ProcessAction()
    
    # Cleans up curses on exit
    @staticmethod
    def CleanupCurses():
        try:
            curses.curs_set(0)
            curses.nocbreak()
            Core.stdscr.keypad(0)
            curses.echo()
            curses.endwin()
        except:
            # TODO: add universal logging (especially for dev)
            pass # exit anyways
    
    # Initializes the curses library for use, and registers cleanup
    @staticmethod
    def InitCurses():
        # First register proper cleanup of curses
        atexit.register(Core.CleanupCurses)
        
        # Next initialize curses for use
        Core.stdscr = curses.initscr()
        curses.curs_set(1)
        curses.cbreak()
        curses.noecho()
        Core.stdscr.keypad(1)

