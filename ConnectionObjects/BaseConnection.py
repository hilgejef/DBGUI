###############################################################################
# BaseConnection
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
#		- DBType
#
#
###############################################################################

from ResultStatus import ResultStatus

class BaseConnection:
    def __init__(self, user, password, host, port, database, dbtype=""):
        self.User = user
        self.Password = password
        self.Host = host
        self.Port = port
        self.Database = database
        self.Connection = None
        self.DBType = dbtype
    
    # Opens a connection to the DB server. To be overloaded in children.  
    def Connect(self):
        return ResultStatus(False, "Unimplemented base function")
    
    # Allows for query execution from a string.To be overloaded in children.
    # WARNING: Open to SQL injection.  Use with care.
    def QueryString(self, query):
        return ResultStatus(False, "Unimplemented base function")
    
    # Allows for buffered query execution. To be overloaded in children.
    # SQL injection safe.
    def QueryBuffered(self, query, values):
        return ResultStatus(False, "Unimplemented base function")
    
    # Parses the results of a query into a format that can be used by the 
    # DataTable widget.
    def ParseResults(self, results):
        return None
