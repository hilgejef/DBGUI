from MySQLConnection import MySQLConnection

my = MySQLConnection("root", "<PASSWORD>")

my.Connect()
my.QueryString("use tmptest")

print "Success!"