################################################################
# Authors: 		Rich Gagliano, Jonathan Moore, Jeffrey Hilger
# Date Created: 	10/24/2015
# Date Modified:	10/24/2015
# File Name:		CursesDatabase.py
#
# Overview:
#	TODO: Project overview
#
################################################################

from CDBCore import CDBCore

if __name__ == "__main__":
    CDBCore.InitCurses(True)
    CDBCore.InitColor()
    CDBCore.InitScreens()
    CDBCore.Main()