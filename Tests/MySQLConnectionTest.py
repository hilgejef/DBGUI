from MySQLConnection import MySQLConnection

# Create the connection object
my = MySQLConnection("root", "<PASSWORD>")

# Attempt to connect
if not my.Connect():
    exit(1)

# Create a database if it does not exist already
my.QueryString("CREATE DATABASE IF NOT EXISTS tmptest")

# Use the database
my.QueryString("USE tmptest")

# Drop the Person table if it already exists
my.QueryString("DROP TABLE IF EXISTS Person")

# Create the Person table fresh
my.QueryString("""
    CREATE TABLE Person (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(30) NOT NULL,
    lastname VARCHAR(30) NOT NULL,
    email VARCHAR(50))
""")

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
my.QueryBuffered(query, values)

print "Success!"