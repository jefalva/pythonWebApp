#!/usr/bin/python3
#enable debugging - BEGIN
import cgi
import cgitb
import sqlite3
cgitb.enable() (display=0, logdir="/home/server/logs")
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
if "accountnum" not in data or "name" not in data:
	print("Error. Please try again.")
else:
	v = "true"

#v = true means validation is OK
if v == "true":
	name = data['name'].value
	accountnum = data['accountnum'].value
	conn = sqlite3.connect('/home/server/sqlite3/banker')
	c = conn.cursor()
	#checking DB for t
	#t = true when there is a match
	for row in c.execute('SELECT * FROM accounts;'):
		x = str(row[0])
		y = str(row[1])
	#checking if there's a match
		if (x,y) == (accountnum,name):
			t = "true"
			break

	#deposit money
	if "balsubmit1" in data and t == "true":
		addmoney = data['enterdeposit'].value
		print("You have updated the balance on this account. <br>")
		for row in c.execute('SELECT * FROM accounts WHERE accountnum=? AND name=?', (accountnum,name)):
			print("<b>Account Number: </b>" + row[0] + "<br>")
			print("<b>Customer Name: </b>" + row[1] + "<br>")
			print("<b>Previous Balance: </b>" + str(row[2]) + "<br>")
		#working non-secure problem code
		#c.execute('UPDATE accounts SET balance = balance + ' + addmoney + ' WHERE accountnum=\'' + accountnum + '\' AND name=\''+ name + '\';')
		c.execute('UPDATE accounts SET balance = balance + ? WHERE accountnum=? AND name=?', (addmoney,accountnum,name))
		conn.commit()
		for row in c.execute('SELECT * FROM accounts WHERE accountnum=? AND name=?', (accountnum,name)):
			print("<b>New Balance: </b>" + str(row[2]) + "<br>")

		with open (fpath, "a") as f:
			f.write("Update DB deposit#time:" + time + "#user:" + name + "\n")

	#withdraw money
	elif "balsubmit2" in data and t == "true":
		submoney = data['enterwithdraw'].value
		print("You have updated the balance on this account. <br>")
		for row in c.execute('SELECT * FROM accounts WHERE accountnum=? AND name=?', (accountnum,name)):
			print("<b>Account Number: </b>" + row[0] + "<br>")
			print("<b>Customer Name: </b>" + row[1] + "<br>")
			print("<b>Previous Balance: </b>" + str(row[2]) + "<br>")
		#working non-secure problem code
		#c.execute('UPDATE accounts SET balance = balance - ' + submoney + ' WHERE accountnum=\'' + accountnum + '\' AND name=\''+ name + '\';')
		c.execute('UPDATE accounts SET balance = balance - ? WHERE accountnum=? AND name=?', (submoney,accountnum,name))
		conn.commit()
		for row in c.execute('SELECT * FROM accounts WHERE accountnum=? AND name=?', (accountnum,name)):
			print("<b>New Balance: </b>" + str(row[2]) + "<br>")

		with open (fpath, "a") as f:
			f.write("Update DB withdrawal#time:" + time + "#user:" + name + "\n")


	else:
		print("Cannot complete transaction. <br> Please try again. <br>")

	conn.close()
print("<a href=\"/index.html\">Back to login page</a>")


