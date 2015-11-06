###############################################################################
# Author:		Rich Gagliano
# Date Created:		11/2/2015
# Date Modified:	11/5/2015
# File Name:		MySQLConnection.py
#
# Overview:
#	Provides a connection object for MySQL databases.
#
###############################################################################

import mysql.connector
from ResultStatus import ResultStatus
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
            return ResultStatus()
        except mysql.connector.Error as ex:
            result = ResultStatus(False, "Could not connect to database: ")
            
            if ex.errno == 1044:
                result.Message += "Invalid username or password."
            elif ex.errno == 1049:
                result.Message += "Database does not exist."
            else:
                result.Message += str(ex)
            return result
             
    # Internal query function to handle both buffered and string queries
    # (I wanted to keep string and buffered queries separate as a mental 
    #  check to ensure we are using the appropriate one in our application.
    #  You could call _Query() directly, but this was not the intent.)
    def _Query(self, query, values = None):
        try:
            cursor = self.Connection.cursor()
            if values is None:
                cursor.execute(query)
            else:
                cursor.execute(query, values)
            self.Connection.commit()
            cursor.close()
            data = self.ParseResults(cursor) 
            return ResultStatus(True, None, data)
        except Exception as ex:
            print ResultStatus(False, "Could not execute query:\n" + str(ex))
    
    # Executes a given query within the database. Open to SQL injection.
    def QueryString(self, query):
        return self._Query(query)
    
    # Executes a given buffered query within the database.
    def QueryBuffered(self, query, values):
        return self._Query(query, values)
    
    # Parses the results of a query into a format that can be used by the 
    # DataTable widget.
    def ParseResults(self, results):
        # TODO: Develop parsing algorithm
        return None
        