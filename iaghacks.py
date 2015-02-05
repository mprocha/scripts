import smtplib
import StringIO
import socket

class Postman(object):
    SERVER    = "smtp.gmail.com"
    USUARIO   = "obsistec@gmail.com"
    SENHA     = "sisobsistecunb"
    MENSSAGEM = None

    @staticmethod
    def getnewmessagebody():
        # Kill the current buffer
        #
        if Postman.MENSSAGEM:
            Postman.MENSSAGEM.close()
        return Postman.getmessagebody()

    @staticmethod
    def getmessagebody():
        # Init the buffer
        #
        if not Postman.MENSSAGEM:
            Postman.MENSSAGEM = StringIO.StringIO()

        # Return a buffer
        #
        return Postman.MENSSAGEM

    @staticmethod
    def send(users, subject):

        # Users as list
        #
        if type(users) == str:
            if users.find(",") == -1:
                users = [ users ]
            else:
                users = users.split(",")
        elif type(users) == list:
            pass
        else:
            raise Exception("User list is invalid")

        # Build message
        #
        subject =  "%s: %s" % (socket.gethostname(), subject)
        message = 'Subject: %s\n\n%s' % (subject, Postman.MENSSAGEM.getvalue())

        # Server
        #
        server = smtplib.SMTP(Postman.SERVER, 587)
        server.starttls()

        # Log in
        #
        server.login(Postman.USUARIO, Postman.SENHA)

        # Dispatch
        #
        server.sendmail(Postman.USUARIO, users, message)

        # Clear mesasge
        #
        if Postman.MENSSAGEM:
            Postman.MENSSAGEM.close()

        return
