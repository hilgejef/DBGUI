################################################################
# CursesDatabase
#
# Overview:
#	CS419 Capstone submission for Group 10.
#
################################################################
import sys
sys.path.append("app")
from CDBCore import CDBCore

if __name__ == "__main__":
    CDBCore.InitCurses()
    CDBCore.InitColor()
    CDBCore.InitScreens()
    CDBCore.Main()