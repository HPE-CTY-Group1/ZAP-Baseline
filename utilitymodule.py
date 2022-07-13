# Authors: Mohit Raj, Shomik Ghosh
import re
import os
import smtplib
import getpass


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def sendmail(target_site):
    #getting the source address from .env
    fromaddr = os.getenv("FROMADDR")

    #getting applicaton specific password of source address
    email_pass= getpass.getpass(prompt='Enter password ')
    
    #input destination address
    toaddr =input("Enter Destination email address: ")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    if(re.fullmatch(regex, toaddr)):
        print("Sending email...")
    else:
        print("Invalid Email")
        quit()

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = f"[REPORT] {target_site}"

    # string to store the body of the mail
    body = f"The report for site {target_site} is attached on this mail"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "testreport.html"
    attachment = open("testreport.html", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.mail.yahoo.com', 587)

    #    start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, email_pass)

    

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()
    
    print("[LOG] Mail sent")

    #close the attachment
    attachment.close()

