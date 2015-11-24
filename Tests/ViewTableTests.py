import sys
from CDBCore import CDBCore
from MySQLConnection import MySQLConnection
from ViewTables import ViewTables
from MainMenu import MainMenu

if __name__ == "__main__":
	user = raw_input('Enter the MySQL db user: ')
	password = raw_input('Enter the MySQL db user password: ')

	my = MySQLConnection(user, password)    
	my.Connect()
	CDBCore.InitCurses(debug=True)
	CDBCore.InitColor()
	CDBCore.Connection = my
	CDBCore.MenuScreen = MainMenu()
	CDBCore.CurrentScreen = ViewTables("tmptest")
	CDBCore.Main()