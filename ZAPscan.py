from json import load
import subprocess
import os
import smtplib
import time
import getpass
from dotenv import load_dotenv
load_dotenv()


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


cwd_path = os.getcwd()


target_site = input("Enter Target Site: ")

def main():
    cmd = f'docker run -v {cwd_path}:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t {target_site} -r testreport.html'
    proc_cmd = cmd.split(' ')

    process = subprocess.Popen(proc_cmd, stdout=subprocess.PIPE)

    for line in iter(process.stdout.readline, ""):
        line = line.decode()
        proc_running = process.poll() is None
        if not proc_running:
            break

        print("[ZAP]", line[:-1])


    if os.path.exists('testreport.html'):
        print("[LOG] Test report generated successfully")
    else:
        print("[ERR] Test report generation failed")

    fromaddr = os.getenv("FROMADDR")

    email_pass= getpass.getpass(prompt='Enter password ')
    
    toaddr =input("Enter Destination email address: ")

    
    
    #email_pass = "ihna lsxk blyz lini"

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

    attachment.close()

    os.remove('testreport.html')

    time.sleep(3)
        
if __name__ == "__main__":
    main()
