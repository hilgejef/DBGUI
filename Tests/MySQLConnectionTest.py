from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection

# Checks the result, and aborts with message if error has
# occured
def CheckResult(result):
    if not result.Success:
        print result.Message
        exit(1)


# Get the user's password
user = raw_input('Enter the MySQL db user: ')
password = raw_input('Enter the MySQL db user password: ')
        
# Create the connection object
my = MySQLConnection(user, password)

# Attempt to connect
result = my.Connect()
CheckResult(result)

# Create a database if it does not exist already
result = my.QueryString("CREATE DATABASE IF NOT EXISTS tmptest")
CheckResult(result)

# Use the database
result = my.QueryString("USE tmptest")
CheckResult(result)

# Drop the Person table if it already exists
result = my.QueryString("DROP TABLE IF EXISTS Person")
CheckResult(result)

# Create the Person table fresh
result = my.QueryString("""
	  CREATE TABLE Person (
	  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	  firstname VARCHAR(30) NOT NULL,
	  lastname VARCHAR(30) NOT NULL,
	  email VARCHAR(50))
      """)
CheckResult(result)
      
# Construct a buffered query
first = "John"
last = "Doe"
email = "john.doe@person.com"
values = [first, last, email]
query = """
	  INSERT INTO Person (firstname, lastname, email)
	  VALUES (%s, %s, %s)
      """

# Execute the buffered query
result = my.QueryBuffered(query, values)
CheckResult(result)

print "Success!"