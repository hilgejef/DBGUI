###############################################################################
# Author:		Rich Gagliano
# Date Created:		12/3/2015
# Date Modified:	12/3/2015
# File Name:		PostgresConnection.py
#
# Overview:
#	Provides a connection object for PostgresSQL databases.
#
###############################################################################

import psycopg2
from ResultStatus import ResultStatus
from BaseConnection import BaseConnection

class PostgresConnection(BaseConnection):
    # PostgresConnection constructor
    def __init__(self, user, password, database = None, host = "127.0.0.1", port = 5432):
        BaseConnection.__init__(self,user, password, host, port, database, "PostgreSQL")
    
    # PostgresConnection destructor
    def __del__(self):
        self.Disconnect()
    
    # Opens a connection to the DB server.
    def Connect(self):
        try:
            # If no database has been specified, omit from connection string
            conn_string = ""
            if self.Database == None:                
                conn_string = "host='" + self.Host + "' user='" + self.User + "' password='" + self.Password + "' port=" + str(self.Port)
            else:
                conn_string = "host='" + self.Host + "' dbname='" + self.Database + "' user='" + self.User + "' password='" + self.Password + "' port=" + str(self.Port)
            self.Connection = psycopg2.connect(conn_string)
            return ResultStatus()
        except Exception as ex:
            result = ResultStatus(False, "Could not connect to database: ")
            result.Message += str(ex)
            return result
    
    # Disconnects from the database
    def Disconnect(self):
        try:
            self.Connection.close()
        except Exception as ex:
            #print "Could not close database connection:\n" + str(ex) #TODO: Status notification?
            pass
    
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
            data = self.ParseResults(cursor) 
            cursor.close()
            return ResultStatus(True, None, data)
        except Exception as ex:
            return ResultStatus(False, "Could not execute query:\n" + str(ex))
    
    # Executes a given query within the database. Open to SQL injection.
    def QueryString(self, query):
        return self._Query(query)
    
    # Executes a given buffered query within the database.
    def QueryBuffered(self, query, values):
        return self._Query(query, values)
    
    # Parses the results of a query into a format that can be used by the 
    # DataTable widget.
    # NOTE: Current structure uses a list in the following format
    #		list[0]: list of headers
    #		list[1]: list of list of data rows
    #
    #	    This was chosen for performance.  If we decide to parse into Labels
    #	    here, this will change to a loop.  Problem is identifying coordinates
    #	    of each Label.  I would think the DataTable widget should handle this,
    #	    so I am just returning the data here to be utilized later.
    def ParseResults(self, cursor):
        try:
            cells = []
            
            # Append the headers
            headers = []
            for header in cursor.description:
                headers.append(header[0])
            cells.append(headers)
            
            # Append the data rows
            cells.append(cursor.fetchall())
                        
            # Return the results
            return cells
        except:
            # Error parsing data, this sould indicate that this was not a
            # SELECT query.  Return None
            return None
            
    # Sets the connection to use a new database
    def SetDatabase(self, database):
        try:
            self.Disconnect()
            self.Database = database
            self.Connect()
            return ResultStatus()
        except Exception as ex:
            result = ResultStatus(False, "Could not connect to database: ")
            result.Message += str(ex)
            return result
    
    def GetDatabases(self):
        return self.QueryString("""SELECT pg_database.datname as "Database" FROM pg_database""")
    
    def GetTables(self):
        return self.QueryString("""SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'""")

    def DescribeTable(self, tblName):
        return self.QueryString("""SELECT column_name, data_type, character_maximum_length FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}'""".format(tblName))