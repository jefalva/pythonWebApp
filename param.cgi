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
data = cgi.FieldStorage()
username = data['username'].value
password = data['password'].value
#-insert input validation here-
#-arbitrary sample entries below-
# to be connected to DB ofc
if (username,password)==("admin","admin"):
	print("<h1>Test Bank</h1>")
	print("Welcome <b>" + username + "! </b><br>")
	print("<b>Accounts Summary</b> <br>")
	print("<table style=\"width100%\">")
	print("<th>Account Number</th>")
	print("<th>Name</th>")
	print("<th>Balance</th>")
	conn = sqlite3.connect('banker')
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
	print("<b>Total Balance: </b>" + str(total))
	print("<br>")
	print("<br>")
	print("<br>")
	print("<form action=\"\">")
	print("Customer's Account Number: <input type=\"text\" name=\"accountnum\"/><br>")
	print("Customer's Name: <input type=\"text\" name=\"name\"/><br>")
	print("<input type=\"submit\" name=\"submit\" value=\"Update Customer Balance\"/>")
	print("</form>")

else:
	print("You have entered a wrong username or password. Please try again.")

