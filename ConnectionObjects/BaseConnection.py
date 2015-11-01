###############################################################################
# Author:		Rich Gagliano
# Date Created:		11/1/2015
# Date Modified:	11/1/2015
# File Name:		BaseConnection.py
#
# Overview:
#	Provides the base connection framework for specific DB connection
#	objects. (To include MySQL and PostgreSQL).
#
#	Choosing to limit common attributes to:
#		- Username
#		- Password
#		- Host
#		- Port
#		- Database
#
#
###############################################################################

class BaseConnection:
    def __init__(self, user, password, host = None, port = None, database = None):
        self.User = user
        self.Password = password
        self.Host = host
        self.Port = port
        self.database = database
    
    # Opens a connection to the DB server. To be overloaded in children.  
    def Connect(self):
        return False # TODO: Update with result status object as return value
    
    # Allows for query execution from a string.To be overloaded in children.
    # WARNING: Open to SQL injection.  Never use with user input.
    def QueryString(self, query):
        return False # TODO: Update with result status object as return value
    
    # Allows for buffered query execution. To be overloaded in children.
    # SQL injection safe.
    def QueryBuffered(self, query, values):
        return False # TODO: Update with result status object as return value
    
    # Parses the results of a query into a format that can be used by the 
    # DataTable widget.
    def ParseResults(self, results):
        return False # TODO: Update with result status object as return value
