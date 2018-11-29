#!/usr/bin/python3
#enable debugging - BEGIN
import cgi
import cgitb
import sqlite3
import re
import hashlib
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
	passoldhash = hashlib.md5(passold.encode('utf-8')).hexdigest()
	passchange = data['passconfirm'].value
	passchangehash = hashlib.md5(passchange.encode('utf-8')).hexdigest()
	conn = sqlite3.connect('/home/server/sqlite3/banker')
	c = conn.cursor()
	#checking DB for t
	#t = true when there is a match
	for row in c.execute('SELECT * FROM users;'):
		x = str(row[0])
		y = str(row[1])
	#checking if there's a match
		if (x,y) == (user,passoldhash):
			t = "true"
			break

	#withdraw money
	if "passconfirm" in data and t == "true":
		#print("You have updated the password on this account. <br>")
		for row in c.execute('SELECT * FROM users WHERE users=(?) AND password=(?)', (user,passoldhash)):
			print("<b>Username: </b>" + row[0] + "<br>")
			#print("<b>Old Password: </b>" + row[1] + "<br>")
			#print("<b>New Password: </b>" + passchange + "<br>")
		#Unsecure, concatenated SQL problem code
		#c.execute('UPDATE users SET password =\'' + passchange + '\' WHERE users=\'' + user + '\' AND password=\'' + passold + '\';')
		c.execute('UPDATE users SET password=? WHERE users=? AND password=?', (passchangehash,user,passoldhash))
		conn.commit()
		print("You have successfully updated your password.")
		#used code below to check if working...
		#for row in c.execute('SELECT * FROM users WHERE users=(?) AND password=(?)', (user,passchangehash)):
			#print("<b>New Password: </b>" + str(row[1]) + "<br>")

	else:
		print("Cannot complete task. <br> Please try again. <br>")

	conn.close()

print("<a href=\"/index.html\">Back to login page</a>")
