#########################################################
# Initial take on program flow. will be tested and
# modified once screens are made.
#
# 
#
#########################################################

import sys
import curses
import atexit
from MainMenu import MainMenu
from HomeScreen import HomeScreen
from StatusScreen import StatusScreen
from PopUp import PopUpOkCancel # TESTING ONLY

class CDBCore:
    # Constants for Defining Screen Locations
    TERMINAL_LINES = 24
    TERMINAL_CHARACTERS = 80
    
    MAIN_MENU_Y = 0         # Main menu display - Lines 0 - 2
    MAIN_MENU_LINES = 3
    MAIN_SCREEN_Y = 3       # Main screen display - Lines 3 - 20
    MAIN_SCREEN_LINES = 18
    STATUS_SCREEN_Y = 21    # Status screen display - Lines 21 - 24
    STATUS_SCREEN_LINES = 4
    
    # Contains the main curses window
    stdscr = ""
  
    # TODO: set to base connection string object
    ConnectionString = ""

    # Overriden by Connection object in ConnectionWizard
    Connection = ""
    
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
        # # CTRL + TAB denotes go back to previous screen if there is one
        elif key in [1]: # TODO: identify CTRL+TAB key possibilities
            if len(CDBCore.History) > 0:
                if CDBCore.CurrentScreen != CDBCore.MenuScreen:
                    CDBCore.CurrentScreen.Hide()
                CDBCore.CurrentScreen = CDBCore.History.pop()
                CDBCore.CurrentScreen.Show()
        # Access Main Menu -  SHIFT-M or F1
        elif key in [curses.KEY_F1, 77]:
            CDBCore.CurrentScreen.UnHighlight()
            CDBCore.CurrentScreen.Update()
            if CDBCore.CurrentScreen.Type == "MainMenu":
                CDBCore.CurrentScreen = CDBCore.History.pop()
            else:
                CDBCore.History.append(CDBCore.CurrentScreen)
                CDBCore.CurrentScreen = CDBCore.MenuScreen
            CDBCore.CurrentScreen.MakeActive()
        else:
            # TODO: Popup to notify user before exitting application that an issue occured
            pass
    
    # Used to change to a new CurrentScreen
    @staticmethod
    def ChangeCurrentScreen(screen):
        CDBCore.History.append(CDBCore.CurrentScreen)
        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = screen
        CDBCore.CurrentScreen.Show()
    
    # Used to test final program flow
    @staticmethod
    def FinalMain(debug=False):      
        # Prepare curses for use
        CDBCore.InitCurses(debug)
        CDBCore.InitColor()
        CDBCore.InitScreens()
        
        # Show the home screen
        CDBCore.CurrentScreen.Show()
        # Show the main menu
        CDBCore.MenuScreen.Show()
        # Show the status screen
        CDBCore.StatusScreen.Show()
        # Process any further actions from the user
        while True:
            CDBCore.ProcessAction()
    
    # Used to test singular screens
    @staticmethod
    def Main():      
        # Prepare curses for use
        #InitCurses()
        
        # Show the home screen
        CDBCore.CurrentScreen.Show()
        # Show the main menu
        CDBCore.MenuScreen.Show()
        # Show the status screen
        CDBCore.StatusScreen.Show()
        
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
    def InitCurses(debug=False):
        # First register proper cleanup of curses
        if not debug:
            atexit.register(CDBCore.CleanupCurses)
        
        # Next initialize curses for use
        CDBCore.stdscr = curses.initscr()

        # Initialize color
        curses.start_color()

        try:
            # Not all terminals support hiding the cursor
            curses.curs_set(1)
        except:
            pass
        curses.cbreak()
        curses.noecho()
        CDBCore.stdscr.keypad(1)

    # Create color pairings and initialize screen background
    @staticmethod
    def InitColor():
        # Text color/text background
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)

        # Window background/window border
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)

        # Screen background/screen border
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_CYAN)

        # Initialize main background color
        CDBCore.stdscr.bkgd(' ', curses.color_pair(3))
        CDBCore.stdscr.box()

    # Initialize screens and objects
    @staticmethod
    def InitScreens():
        CDBCore.MenuScreen = MainMenu()
        CDBCore.CurrentScreen = HomeScreen()
        CDBCore.StatusScreen = StatusScreen()