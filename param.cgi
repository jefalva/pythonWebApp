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

#v is for "validation is okay"
v = "false"

#regex that tests if alphanumeric & underscore & 1 to 10 chars
regex = re.compile("^[a-zA-Z0-9_]{1,10}$")

#data = entries from pervious form
data = cgi.FieldStorage()
#IS THERE EVEN ANY INPUT FROM param.cgi!? DAMNIT WHY THEY LEAVE IT BLANK...
if "username" not in data or "password" not in data:
	print("Username or password cannot be blank. Please try again.")
	print("<a href=\"/index.html\">Return to login page</a>")
else:
	#GOOD. THANCC YOU. Let's assign these variables:
	username = data['username'].value
	password = data['password'].value
	#YES. IT FITS THE REGEX
	if regex.match(username):
		v = "true"
	#IS THIS INPUT FOLLOWING MY RULEZ!? WHY U NO FOLLOW?
	else:
		print("Usernames can only be 1-10 letters, numbers and underscores.")
		print(" Please try again.")
		print("<a href=\"/index.html\">Return to login page</a>")

#v = true means validation OK
if v == "true":
	conn = sqlite3.connect('/home/server/sqlite3/banker')
	c = conn.cursor()
	#initializing userq and passq
	userq = "false"
	passq = "false"
	#IS USERNAME IN HERE!?
	for row in c.execute('SELECT * FROM users;'):
		x = str(row[0])
		if x == username:
			userq = username
	row = ""
	#NO! USERNAME IS NOT IN DATABASE!
	if userq == "false":
		print("Wrong username or password. Please try again.")
		print("<a href=\"/index.html\">Return to login page</a>")
	#YES! USERNAME IS HERE!
	else:
		#IS THE PASSWORD EVEN CORRECT!?
		for row in c.execute('SELECT password FROM users WHERE users=?', (userq,)):
			x = str(row[0])
			xhash = hashlib.md5(x.encode('utf-8')).hexdigest()
			passq = xhash
			#passq = x
		
		#IF USERNAME AND PASSWORD IS CORRECT, THEN
		if (username,password)==(userq,passq):
			#check the type of account
			for row in c.execute('SELECT type FROM users WHERE users=?', (userq,)):
				type = str(row[0])
			
			#if an "admin"
			if (username,password,type)==(userq,passq,"admin"):
				print("<h1>Test Bank</h1>")
				print("Welcome <b>" + username + "! </b><br>")
				print("<b>Accounts Summary</b> <br>")
				print("<table style=\"width100%\">")
				print("<th>Account Number</th>")
				print("<th>Name</th>")
				print("<th>Balance</th>")
				conn = sqlite3.connect('/home/server/sqlite3/banker')
				c = conn.cursor()
				total = 0
				for row in c.execute('SELECT * FROM accounts'):
					print("<tr>")
					print("<td>" + row[0] + "</td>")
					print("<td>" + row[1] + "</td>")
					print("<td>" + str(row[2]) + "</td>")
					print("</tr>")
					total = total + row[2]
				print("</table>")
				#SHOW ME DA MONEY!
				print("<b>Total Balance: </b>" + str(total))
				print("<br>")
				print("<br>")
				print("<br>")
				print("<form id=\"updatingbal\" action=\"balance.cgi\" method=\"POST\" AUTOCOMPLETE='OFF'>")
				print("Customer's Account Number: <input type=\"text\" name=\"accountnum\"/><br>")
				print("Customer's Name: <input type=\"text\" name=\"name\"/><br>")
				print("Deposit an amount: <input type=\"number\" step=\"0.01\" name=\"enterdeposit\"/>")
				print("<input type=\"submit\" name=\"balsubmit1\" value=\"Deposit Amount\"/>")
				print("<br>")
				print("Withdraw an amount: <input type=\"number\" step=\"0.01\" name=\"enterwithdraw\"/>")
				print("<input type=\"submit\" name=\"balsubmit2\" value=\"Withdraw Amount\"/>")
				print("</form>")
				print("<p><a href=\"/index.html\">Return to login page</a>")

			#if one of the ordinary "users"
			if (username,password,type)==(userq,passq,"users"):
				print("<h1>Test Bank</h1>")
				print("Welcome <b>" + username + "! </b><br>")
				print("<b>Account Summary</b> <br>")
				conn = sqlite3.connect('/home/server/sqlite3/banker')
				c = conn.cursor()
				for row in c.execute('SELECT * FROM accounts INNER JOIN users ON users.accountnum = accounts.accountnum WHERE users=?', (userq,)):
					print("Your account balance is: " + str(row[2]))
				print("<p><a href=\"/password_change.html\">Update your password here</a>")
				print("<p><a href=\"/index.html\">Back to login page</a>")
		
		#IF USERNAME OR PASSWORD IS WRONG, THEN
		else:
			print("Wrong username or password. Please try again.")
			print("<a href=\"/index.html\">Return to login page</a>")

conn.close()
