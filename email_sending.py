import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib, ssl
from email.mime.text import MIMEText # New line
from email.utils import formataddr
import os







#setups email information 
#senders account info usr & PW 
emailfrom = "dickandspence@gmail.com"
password = "latvain123"


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
            status = False
        except Exception as e:
            status = True
            print(f'Oh no! Something bad happened!n {e}')
        finally:
            
            server.quit()
    except Exception as e:
        status = True
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
        server.sendmail(emailfrom, send_to, msg.as_string())
        status = "warning sent"
    except Exception as e:
        print(e)
        status = "failed to send following error: {e}"
    finally:
        server.quit()
    return status

def sendall():
            global emailfrom
            global password    

            sender_email = 'laose152@gmail.com' #dump email, if using gmail remember to turn on less secure app access on setting; other email remember to change the line 378
            sender_name = 'LAB WATCH'
            password = 'Xx1387011247'
            receiver_email = 'laose152@gmail.com'
            receiver_name = 'Rob'
            # Email text
            email_body = '''
                These are all the report 
            '''
            filename = 'zip2.zip' # for testing change it to the path of the file u want to send
            print("Sending the email...")
            # Configurating user's info
            msg = MIMEMultipart()
            msg['To'] = formataddr((receiver_name, receiver_email))
            msg['From'] = formataddr((sender_name, sender_email))
            msg['Subject'] = 'Hello, my friend ' + receiver_name
            msg.attach(MIMEText(email_body, 'plain'))
            try:
                    # Open PDF file in binary mode
                    with open(filename, "rb") as attachment:
                                    part = MIMEBase("application", "octet-stream")
                                    part.set_payload(attachment.read())

                    # Encode file in ASCII characters to send by email
                    encoders.encode_base64(part)

                    # Add header as key/value pair to attachment part
                    part.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {filename}",
                    )

                    msg.attach(part)
            except Exception as e:
                    print(f'Oh no! We didnt found the attachment!n{e}')
                                          
            try:
                    # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
                    server = smtplib.SMTP('smtp.office365.com', 587) #depend on the eail change smtp.gmail.com to smtp.xxxxx.com; outlook email : smtp.office365.com
                    # Encrypts the email
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                    # We log in into our Google account
                    server.login(sender_email, password)
                    # Sending email from sender, to receiver with the email body
                    server.sendmail(sender_email, receiver_email, msg.as_string())
                    print('Email sent!')
            except Exception as e:
                    print(f'Oh no! Something bad happened!n {e}')
            finally:
                    print('Closing the server...')
                    server.quit()
                    
          