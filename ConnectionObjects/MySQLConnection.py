###############################################################################
# Author:		Rich Gagliano
# Date Created:		11/2/2015
# Date Modified:	11/2/2015
# File Name:		MySQLConnection.py
#
# Overview:
#	Provides a connection object for MySQL databases.
#
###############################################################################

import mysql.connector
from BaseConnection import BaseConnection

class MySQLConnection(BaseConnection):
    # MySQLConnection constructor
    def __init__(self, user, password, host = "127.0.0.1", port = 3306, database = None):
        BaseConnection.__init__(self,user, password, host, port, database)
    
    # MySQLConnection destructor
    def __del__(self):
        try:
            self.Connection.close()
        except Exception as ex:
            print "Could not close database connection:\n" + str(ex) #TODO: Status notification
    
    # Opens a connection to the DB server.
    def Connect(self):
        try:
            # If no database has been specified, omit from connection string
            if self.Database == None:
                self.Connection = mysql.connector.connect(user=self.User,
                                                          password=self.Password,
                                                          host=self.Host,
                                                          port=self.Port)
            else:
                self.Connection = mysql.connector.connect(user=self.User,
                                                          password=self.Password,
                                                          host=self.Host,
                                                          port=self.Port,
                                                          database=self.Database)
        except mysql.connector.Error as ex:
            msg = "Could not connect to database: "
            
            if ex.errno == 1044:
                msg += "Invalid username or password."
            elif ex.errno == 1049:
                msg += "Database does not exist."
            else:
                msg += str(ex)
            print msg #TODO: Popup, and status notification
                                                  
    # Executes a given query within the database. Open to SQL injection.
    def QueryString(self, query):
        try:
            cursor = self.Connection.cursor()
            cursor.execute(query)
            cursor.close()
            data = self.ParseResults(cursor) # Store these results in result status object
            return True # TODO: Update with result status object as return value
        except Exception as ex:
            print "Could not execute query:\n" + str(ex) #TODO: Wrap into ResultStatusObject
    
    # Executes a given buffered query within the database.
    def QueryBuffered(self, query, values):
        return False # TODO: Update with result status object as return value
    
    # Parses the results of a query into a format that can be used by the 
    # DataTable widget.
    def ParseResults(self, results):
        # TODO: Develop parsing algorithm
        return None
        