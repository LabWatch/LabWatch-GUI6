import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os


#setups email information 
#account email is coming from 
emailfrom = "dickandspence@gmail.com"
#account email is being sent too 
emailto = "saltydick61@gmail.com"

#file to send
fileToSend = "/home/saltyd/LabWatchGUI6/Logging/2021-03.csv"

#senders account info usr & PW 
username = "dickandspence@gmail.com"
password = "latvain123"

msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = "help I cannot send an attachment to save my life"
msg.preamble = "help I cannot send an attachment to save my life"

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

fp = open(fileToSend, "rb")
attachment = MIMEBase(maintype, subtype)
attachment.set_payload(fp.read())
fp.close()
encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(fileToSend))
msg.attach(attachment)
try:
    # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
    server = smtplib.SMTP("smtp.gmail.com:587")
    # Encrypts the email
    server.starttls()
    # We log in into our Google account
    server.login(username,password)
    # Sending email from sender, to receiver with the email body
    server.sendmail(emailfrom, emailto, msg.as_string())
    print('Email sent!')
except Exception as e:
        print(f'Oh no! Something bad happened!n {e}')
finally:
        print('Closing the server...')
        server.quit()