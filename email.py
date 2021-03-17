
import smtplib, ssl
from email.mime.text import MIMEText # New line
from email.utils import formataddr  # New line

# User configuration replce receiver_email with rob's email 
sender_email = 'laose152@gmail.com'
sender_name = 'LAB WATCH'
password = 'Xx1387011247'
receiver_email = 'laose152@gmail.com'
receiver_name = 'Rob'
# Email text
email_body = '''
    Hi the lab room temp is unusual 
'''

print("Sending the email...")
# Configurating user's info
msg = MIMEText(email_body, 'plain')
msg['To'] = formataddr((receiver_name, receiver_email))
msg['From'] = formataddr((sender_name, sender_email))
msg['Subject'] = 'Hello, my friend ' + receiver_name
try:
        # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
        server = smtplib.SMTP('smtp.gmail.com', 587)
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
