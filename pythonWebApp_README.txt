Python Web Application Assignment
---------------------------------
Jeffrey, James, Jomar, Alfred


File Locations
--------------

/usr/lib/cgi-bin/
-----------------
	param.cgi		> login, main dynamic content
	balance.cgi		> updating balance values
	passchange.cgi		> updating passwords for users
	functions.py		> security additions(logging)

/var/www/html/
--------------
	index.html		> landing page, login form
	password_change.html	> password change form

/home/server/sqlite3/
---------------------
	banker			> database

/home/server/python3/
---------------------
	log.txt			> log working with functions.py


Permissions
------------
chmod 755 /usr/lib/cgi-bin/param.cgi
chmod 755 /usr/lib/cgi-bin/balance.cgi
chmod 755 /usr/lib/cgi-bin/passchange.cgi
chmod 775 /home/server/sqlite3
chgrp www-data /home/server/sqlite3
chmod 660 /home/server/sqlite3/banker
chgrp www-data /home/server/sqlite3/banker



Setting Up SSL
--------------
Step 1: Generate a Private Key

The command creates a 1024 bit RSA key encrypted using Triple-Des

Command:
openssl genrsa -des3 -out server.key 1024

YouÅfll be prompted to enter a PEM passphrase and re-enter it to verify

Step 2: Generate a Certificate Signing Request

Command:
openssl req -new -key server.key -out server.csr

YouÅfll be prompted to enter a bunch of information like country name, state, etc

Step 3: Generate a self-signed certificate

Self-signed for our testing purposes. Command creates a temp certificate thatÅfs good for 365 days

Command:
openssl x509 -req -days 365 -in server.csr -out server.crt

Step 4: Copy Private Key and Certificate to a designated path

Commands:
sudo cp server.crt /etc/apache2/conf-enabled/server.crt
sudo cp server.key /etc/apache2/conf-enabled/server.key

Step 5: Make sure ssl is running/enabled

Command:
sudo a2enmod ssl

Step 6: Edit ApacheÅfs SSL configuration file

Command:
sudo nano /etc/apache2/sites-enabled/default-ssl.conf

Edit the lines to match the blue text:
<VirtualHost __default__:443>
DocumentRoot /var/www/
SSLEngine on
SSLCertificateFile /etc/apache2/conf-enabled/server.crt
SSLCertificateKeyFile /etc/apache2/conf-enabled/server.key
</VirtualHost>

*if default-ssl.conf is not found use this command:
sudo cp /etc/apache2/sites-available/default-ssl.conf /etc/apache2/site-enabled/default-ssl.conf

Step 8: Test

Command:
sudo apachectl configtest

Step 9: Restart (Stop and Run)

Commands:
sudo apachectl stop
sudo apachectl start

*If apachectl start doesnÅft work try:
sudo apachectl startssl 

Links/References:
https://www.akadia.com/services/ssh_test_certificate.html

https://www.digicert.com/csr-ssl-installation/ubuntu-server-with-apache2-openssl.htm

https://www.digitalocean.com/community/tutorials/how-to-create-a-ssl-certificate-on-apache-for-ubuntu-14-04


