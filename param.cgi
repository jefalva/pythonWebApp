#!/usr/bin/python3
#enable debugging - BEGIN
import cgi
import cgitb
import sqlite3
import os
import datetime
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
#data = entries from pervious form
data = cgi.FieldStorage()
#IS THERE EVEN ANY INPUT FROM param.cgi!? DAMNIT WHY THEY LEAVE IT BLANK...
if "username" not in data or "password" not in data:
	print("Username or password cannot be blank. Please try again.")
	print("<a href=\"/index.html\">Return to login page</a>")
#GOOD. THANCC YOU.
else:
	v = "true"

#v = true means validation OK
if v == "true":
	username = data['username'].value
	password = data['password'].value
	conn = sqlite3.connect('/home/server/sqlite3/banker')
	c = conn.cursor()
	time = str(datetime.datetime.now())
	fpath = os.path.join("/home/server/python3", "log.txt") #path to log file
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
		for row in c.execute('SELECT password FROM users WHERE users=\'' + userq + '\';'):
			x = str(row[0])
			passq = x
		
		#right now admin is still hard coded...we need to decide how we want to do admin account...
		if (username,password)==("admin","admin"):
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
			print("<form id=\"updatingbal\" action=\"balance.cgi\" method=\"POST\">")
			print("Customer's Account Number: <input type=\"text\" name=\"accountnum\"/><br>")
			print("Customer's Name: <input type=\"text\" name=\"name\"/><br>")
			print("Deposit an amount: <input type=\"number\" step=\"0.01\" name=\"enterdeposit\"/>")
			print("<input type=\"submit\" name=\"balsubmit1\" value=\"Deposit Amount\"/>")
			print("<br>")
			print("Withdraw an amount: <input type=\"number\" step=\"0.01\" name=\"enterwithdraw\"/>")
			print("<input type=\"submit\" name=\"balsubmit2\" value=\"Withdraw Amount\"/>")
			print("</form>")
			with open (fpath, "a") as f:
				f.write("Login DB#time:" + time + "#user:" + username)

		#if login is not admin account,
		#if credentials match DB, user gets in
		#they can view their balance
		elif (username,password)==(userq,passq):
			print("<h1>Test Bank</h1>")
			print("Welcome <b>" + username + "! </b><br>")
			print("<b>Account Summary</b> <br>")
			conn = sqlite3.connect('/home/server/sqlite3/banker')
			c = conn.cursor()
			for row in c.execute('SELECT * FROM accounts INNER JOIN users ON users.accountnum = accounts.accountnum WHERE users=\'' + userq + '\';'):
				print("Your account balance is: " + str(row[2]))
			conn.close()
			with open (fpath, "a") as f:
				f.write("Login DB#time:" + time + "#user:" + username)
		else:
			print("Wrong username or password. Please try again.")
			print("<a href=\"/index.html\">Return to login page</a>")
