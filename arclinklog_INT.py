import smtplib
import mimetypes
import email
import email.mime.application
from os import system, remove
from sys import exit


webreqlog = '/opt/seiscomp3/bin/seiscomp exec python /opt/seiscomp3/lib/python/webreqlog/webreqlog.py --host 164.41.28.154 -d mysql://sysop:sysop@localhost/seiscomp3 --export file:arclinkLOG.html'
system(webreqlog)

# Create a text/plain message
msg = email.mime.Multipart.MIMEMultipart()
msg['Subject'] = 'INTERNAL Arclink LOG!'

# The main body is just another attachment
body = email.mime.Text.MIMEText("""Hello, how are you? I am just sending you these logs!""")
msg.attach(body)


# PDF attachment
logFile = 'arclinkLOG.html'

fp=open(logFile)
att = email.mime.application.MIMEApplication(fp.read(),_subtype="html")
fp.close()
att.add_header('Content-Disposition','attachment',filename=logFile)
msg.attach(att)
print '%s attached' % (logFile)

## Sending Mail...
server = smtplib.SMTP('smtp.gmail.com', 587)
sender = 'obsistec@gmail.com'
receivers = ['bruno@iag.usp.br', 'marcelorocha.unb@gmail.com']
#receivers = ['bruno@iag.usp.br', 'm.tchelo@gmail.com']


#Next, log in to the server and send the email
server.starttls()
server.login("obsistec@gmail.com", "sisobsistecunb")
print 'Sending mail...'
try:
    server.sendmail(sender, receivers, msg.as_string())
    print '...mail sent.'
except:
    'Could not send mail.'

remove(logFile)
