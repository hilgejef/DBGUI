import sys
import curses
from CDBCore import CDBCore
from Label import Label
from Button import Button
from BaseScreen import BaseScreen
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection

class QueryTable(BaseScreen, db_name, table_name):
    def __init__(self):
        BaseScreen.__init__(self, screen_type="QueryTable")
        self.DBName = db_name
        self.TableName = table_name

    def Init(self):
        DBlabel = BaseLabel("Database: " + self.DBName, 4, 1, 3, len("Database : " + self.DBName), 
        	              attr={"boxed": True, "y_offset" : 1, "x_offset": 1, "text_y_center": False, "text_x_center" : False})
        TableLabel = BaseLabel("Table: " + self.TableName, 7, 1, 3, len("Database : " + self.DBName), 
        	              attr={"boxed": True, "y_offset" : 1, "x_offset": 1, "text_y_center": False, "text_x_center" : False})
        self.PassiveWidgets.append(label)