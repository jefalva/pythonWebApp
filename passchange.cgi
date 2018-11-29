#!/usr/bin/python3
#enable debugging - BEGIN
import cgi
import cgitb
import sqlite3
cgitb.enable() #(display=0, logdir="/path/to/logdir")
#enable debugging - END
#HTTP Headers - BEGIN
#set encoding to UTF-8
print("Content-Type: text/html;charset=utf-8")
print()
#HTTP Headers - END
#MAIN--

#initialializing t = false
t = "false"
v = "false"

data = cgi.FieldStorage()



#input str len validation----not working right now
if "name" not in data or "passconfirm" not in data:
	print("Error. Please try again.")
else:
	v = "true"


#v = true means validation is OK
if v == "true":
	user = data['name'].value
	passold = data['passold'].value
	passchange = data['passconfirm'].value
	conn = sqlite3.connect('/home/server/sqlite3/banker')
	c = conn.cursor()
	#checking DB for t
	#t = true when there is a match
	for row in c.execute('SELECT * FROM users;'):
		x = str(row[0])
		y = str(row[1])
	#checking if there's a match
		if (x,y) == (user,passold):
			t = "true"
			break

	#withdraw money
	if "passconfirm" in data and t == "true":
		print("You have updated the balance on this account. <br>")
		for row in c.execute('SELECT * FROM users WHERE users=(?) AND password=(?)', (user,passold)):
			print("<b>Username: </b>" + row[0] + "<br>")
			print("<b>Old Password: </b>" + row[1] + "<br>")
			print("<b>New Password: </b>" + passchange + "<br>")
		c.execute('UPDATE users SET password =\'' + passchange + '\' WHERE users=\'' + user + '\' AND password=\'' + passold + '\';')
		conn.commit()
		for row in c.execute('SELECT * FROM users WHERE users=(?) AND password=(?)', (user,passchange)):
			print("<b>New Password: </b>" + str(row[1]) + "<br>")

	else:
		print("Cannot complete task. <br> Please try again. <br>")





	conn.close()

print("<a href=\"/index.html\">Back to login page</a>")


