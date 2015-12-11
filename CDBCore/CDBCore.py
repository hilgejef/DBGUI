#########################################################
# CDBCore
#
# Handles the program flow
#
#########################################################

import sys
import curses
import atexit
import MainMenu
import HomeScreen
import StatusScreen
from PopUp import PopUpOk

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
  
    # Set to connection string object
    ConnectionString = ""

    # Overriden by Connection object in ConnectionWizard
    Connection = ""
    
    # Set to home screen
    CurrentScreen = ""
    
    # Set to menu screen
    MenuScreen = ""
    
    # Set to status screen
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
        elif key in [curses.KEY_ENTER, ord('\n'), 10]:
            if CDBCore.CurrentScreen.Type == "MainMenu":
                tmpScreen = CDBCore.History[-1]
                tmpScreen.Hide()
                tmpScreen = None
            else:
                CDBCore.History.append(CDBCore.CurrentScreen)
                CDBCore.CurrentScreen.Hide()
            CDBCore.CurrentScreen = CDBCore.CurrentScreen.Next()
            CDBCore.CurrentScreen.Show()
        # Access Main Menu -  SHIFT-M or F1
        elif key in [curses.KEY_F1, 77]:
            CDBCore.CurrentScreen.UnHighlight()
            CDBCore.CurrentScreen.Update()
            if CDBCore.CurrentScreen.Type == "MainMenu":
                CDBCore.StatusScreen.UpdatePersistentMessage("Shift-M: Main Menu", 1)
                CDBCore.CurrentScreen = CDBCore.History.pop()
            else:
                CDBCore.StatusScreen.UpdatePersistentMessage("Shift-M: Exit Main Menu", 1)
                CDBCore.History.append(CDBCore.CurrentScreen)
                CDBCore.CurrentScreen = CDBCore.MenuScreen
            CDBCore.CurrentScreen.MakeActive()
        # Access Status Screen Message Log -  SHIFT-L or F8
        elif key in [curses.KEY_F8, 76]:
            CDBCore.CurrentScreen.UnHighlight()
            if CDBCore.CurrentScreen.Type == "StatusScreen":
                CDBCore.StatusScreen.UpdatePersistentMessage("Shift-L: Message Log", 2)
                CDBCore.CurrentScreen = CDBCore.History.pop()
            else:
                CDBCore.StatusScreen.UpdatePersistentMessage("Shift-L: Exit Message Log", 2)
                CDBCore.History.append(CDBCore.CurrentScreen)
                CDBCore.CurrentScreen = CDBCore.StatusScreen
            CDBCore.CurrentScreen.MakeActive()
        # This means an unhandled character was passed to the core
        # Notify the user that the application is going down...
        else:
            msg = "Unexpected error occured.  Shutting down."
            CDBCore.PopUp = PopUpOk(msg)
            CDBCore.PopUp.MakeActive()
    
    # Used to test final program flow
    @staticmethod
    def FinalMain(debug=False):      
        # Prepare curses for use
        CDBCore.InitCurses(debug)
        CDBCore.InitColor()
        CDBCore.InitScreens()

        CDBCore.StatusScreen.AddStatusMessage("Welcome to Curses Database!")
        
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
        CDBCore.StatusScreen.AddStatusMessage("Welcome to Curses Database!")
        
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
        #check that terminal supports color
        if curses.has_colors():
            # Text color/text background
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

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
        CDBCore.MenuScreen = MainMenu.MainMenu()
        CDBCore.CurrentScreen = HomeScreen.HomeScreen()
        CDBCore.StatusScreen = StatusScreen.StatusScreen()