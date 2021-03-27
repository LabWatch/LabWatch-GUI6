import smtplib, ssl
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from email.utils import formataddr
import os

#setups email information 
#senders account info usr & PW 
emailfrom = "labwatchmonitoring@gmail.com"
password = "Pw$uck3214"


# from datetime import date
from dateutil.relativedelta import relativedelta

#finds last months file to send
#date_file = date.today() + relativedelta(months=0)

def sendfile(send_to,date_file):
    global emailfrom
    global password
    
    status =True

    y_file = date_file.strftime("%Y")
    m_file = date_file.strftime("%m")
    cwd = os.getcwd()
    fileToSend = cwd + "/Logging/{}-{}.csv".format(y_file,m_file)
    # print(fileToSend)
    try:
        #Starts to build email
        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = send_to
        msg["Subject"] = "Month Report for {}-{}".format(y_file,m_file)
        msg.preamble = "Sending CSV file for the Month of {}-{} sensor data".format(y_file,m_file)
        ctype, encoding = mimetypes.guess_type(fileToSend)
    except:
        print("no file found")

    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    
    try:
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
            server.login(emailfrom,password)
            # Sending email from sender, to receiver with the email body
            server.sendmail(emailfrom, send_to, msg.as_string())
            status = False
        except Exception as e:
            status = True
            print(f'Oh no! Something bad happened!n {e}')
        finally:
            
            server.quit()
    except Exception as e:
        print(f'Oh no! Something bad happened!n {e}')
        status = True
    return status

def sendwarning(send_to,temp,humid):
    global emailfrom
    global password
    
    status =""

    
    try:
        email_body = "Laboratory is out of range. The current temperature is {}°C and humidity is {}% ".format(temp,humid)
        # Configurating user's info
        #Starts to build email
        msg = MIMEText(email_body, 'plain')
        msg["From"] = emailfrom
        msg["To"] = send_to
        msg["Subject"] = "WARNING! Laboratory temperature and/or humidity out of Range"
        msg.preamble = "Warning alarm out of range"

        # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
        server = smtplib.SMTP("smtp.gmail.com:587")
        # Encrypts the email
        server.starttls()
        # We log in into our Google account
        server.login(emailfrom,password)
        # Sending email from sender, to receiver with the email body
        server.sendmail(emailfrom, send_to, msg.as_string())
        status = "warning sent"
    except Exception as e:
        print(e)
        status = "Failed to send following error: {e}"
    finally:
        server.quit()
    # return status

def sendall(send_to,filename):
    global emailfrom
    global password
    
    
    try:
        #Starts to build email
        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = send_to
        msg["Subject"] = "Complete Report Summary"
        msg.preamble = "Sending zip of all Log files"
        ctype, encoding = mimetypes.guess_type(filename)
    except:
        print("no file found")

    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    
    try:
        fp = open(filename, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(filename))
        msg.attach(attachment)
        try:
            # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
            server = smtplib.SMTP("smtp.gmail.com:587")
            # Encrypts the email
            server.starttls()
            # We log in into our Google account
            server.login(emailfrom,password)
            # Sending email from sender, to receiver with the email body
            server.sendmail(emailfrom, send_to, msg.as_string())
            status = False
        except Exception as e:
            status = True
            # print(f'Oh no! Something bad happened!n {e}')
        finally:
            
            server.quit()
    except Exception as e:
        status = True
    
