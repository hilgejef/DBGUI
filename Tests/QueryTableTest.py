import sys
from CDBCore import CDBCore
from MySQLConnection import MySQLConnection
from QueryTable import QueryTable
from MainMenu import MainMenu

if __name__ == "__main__":
	user = raw_input('Enter the MySQL db user: ')
	password = raw_input('Enter the MySQL db user password: ')

	my = MySQLConnection(user, password)    
	my.Connect()
	CDBCore.InitCurses(debug=True)
	CDBCore.InitColor()
	CDBCore.Connection = my
	# CDBCore.MenuScreen = MainMenu()
	CDBCore.CurrentScreen = QueryTable("tmptest")
	CDBCore.Main()