import curses
from CDBCore import CDBCore
from MainMenu import MainMenu
from DataScreen import DataScreen
from MySQLConnection import MySQLConnection

db = raw_input('Database type (p for Postgres, m for MySQL: ')
user = raw_input('Enter the db user: ')
password = raw_input('Enter the db user password: ')
database = raw_input('Enter the db database: ')
my = None
if db == "m":
    my = MySQLConnection(user, password, "127.0.0.1", 3306, database)
else:
    my = PostgresConnection(user, password, database)
result = my.Connect()
if result.Success:
    CDBCore.InitCurses(True)
    CDBCore.InitColor()
    CDBCore.InitScreens()
    CDBCore.Connection = my

    result = CDBCore.Connection.QueryString("DESCRIBE test1;")

    CDBCore.CurrentScreen.Hide()
    CDBCore.CurrentScreen = DataScreen(result.Data, majorScreen="ViewTables")
    CDBCore.CurrentScreen.MakeActive()
    CDBCore.Main()
else:
    print "Could not log in: " + result.Message