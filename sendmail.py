#!/usr/bin/python

import smtplib

# Specifying the from and to addresses

fromaddr = 'marcelorocha@unb.br'
toaddrs  = ['marcelorocha.unb@gmail.com'] 

# Writing the message (this message will appear in the email)

msg = 'Test'

# Login

username = 'marcelorocha@unb.br'
password = '21s0ph1@@!'

# Sending the mail  

server = smtplib.SMTP('mail.unb.br',587)
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
