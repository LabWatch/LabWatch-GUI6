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
#senders account info usr & PW 
emailfrom = "dickandspence@gmail.com"
password = "latvain123"


# from datetime import date
# from dateutil.relativedelta import relativedelta

#finds last months file to send
#date_file = date.today() + relativedelta(months=0)

def sendfile(send_to,date_file):
    global emailfrom
    global password
    
    status =""

    y_file = date_file.strftime("%Y")
    m_file = date_file.strftime("%m")
    fileToSend = "/home/saltyd/LabWatchGUI6/Logging/{}-{}.csv".format(y_file,m_file)
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
            status = "Email sent!"
        except Exception as e:
            status = "failed to send following error: {e}"
            print(f'Oh no! Something bad happened!n {e}')
        finally:
            
            server.quit()
    except Exception as e:
        status = "failed to send following error: {e}"
    return status 

def sendwarning(send_to,temp,humid):
    global emailfrom
    global password
    
    status =""

    
    try:
        email_body = "Lab temp is out of range current temp is {} and himid is {} ".format(temp,humid)
        # Configurating user's info
        #Starts to build email
        msg = MIMEText(email_body, 'plain')
        msg["From"] = emailfrom
        msg["To"] = send_to
        msg["Subject"] = "Lab Out of Range Warning"
        msg.preamble = "Warning alarm out of range"

        # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
        server = smtplib.SMTP("smtp.gmail.com:587")
        # Encrypts the email
        server.starttls()
        # We log in into our Google account
        server.login(emailfrom,password)
        # Sending email from sender, to receiver with the email body
        server.sendmail(emailfrom, emailto, msg.as_string())
        status = "warning sent"
    except Exception as e:
        status = "failed to send following error: {e}"
    finally:
        server.quit()
    return status 