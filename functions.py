import os
import datetime
import hashlib

hasher = hashlib.md5()
with open("verif.txt", "rb") as afile:
	buf = afile.read()
	hasher.update(buf)
print(hasher.hexdigest())
def verifysecret():
	"This does secret things with a date and a key to verify identity"
	time = datetime.date.today() #stores the day in the month it is
	fpath = os.path.join("/home/linuxwebapp/python3", "verif.txt") #path to secret
	with open (fpath, "r") as f: # reading file line by line into a list
		content = f.readlines() #reads secret file into content
		content = [x.strip() for x  in content] #trims newline
	return (content[time.day-1]) #returns index from list based on dayofmonth

def verifyevent():
	"This logs verifies acceptable events based on the log"
	fpath = os.path.join("/home/linuxwebapp/python3", "log.txt") #path to log
	with open (fpath, "r") as f: #reading file line by line into a list
		content = f.readlines() #reads secret file into content
		content = [x.strip() for x in content] # trims newline
	if "Login" in content[-1]:
		return 1 #code to send if the last action was a login
	if "Update" in content[-1]:
		return 2 #code tos end if the last action was a transaction
	else:
		return 0 #code to send if last action does not exist
def verifydb():
	"This hashes and checks DB after each recorded event"
	hasher = hashlib.md5()

	fpath = os.path.join("home/linuxwebapp/sqlite3", "banker") #path to DB
	with open(fpath, "rb") as afile:
		buf = afile.read()
		hasher.update(buf)
	print(hasher.hexdigest())
#print (verifyevent())
