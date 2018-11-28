#!/usr/bin/python3
#enable debugging - BEGIN
import cgi
import cgitb
cgitb.enable()
#enable debugging - END
#HTTP Headers - BEGIN
#set encoding to UTF-8
print("Content-Type: text/html;charset=utf-8")
print()
# HTTP Heacers - END
# HTML CONTENT BEGIN
c = conn.cursor(BANKERLOCATION)
data = cgi.FieldStorage()
passold = data['passold'].value
password = data['password'].value
passconfirm = data['passconfirm'].value
for row in c.execute('SELECT * FROM users;'):
  currentpass = str(row[1])
  strikes = str(row[2])
  if ((currentpass == passold) && strikes < 3):
    sql = 'UPDATE users SET pass = + ' + passconfirm + ' WHERE passold=\'' + passold + '\';'
    c.execute(sql)
    conn.commit()
    print("Password succesfully changed!")
  else:
    print("Current password incorrect, try again.")
    sql = 'UPDATE users SET strikes = +' + strikes + 'WHERE user=\'' + user + '\';'
    c.execute(sql)

#print("<h1>Form Test</h1>")
#print("---" + passold + "---")
#print("---" + password + "---")
#print("---" + passconfirm + "---")
#print("<p><b>" + test + "</b></p>")
