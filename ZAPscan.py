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

#getting current working directory path
cwd_path = os.getcwd()

#getting target site input
target_site = input("Enter Target Site: ")

def main():
    #storing the command
    cmd = f'docker run -v {cwd_path}:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t {target_site} -r testreport.html'
    proc_cmd = cmd.split(' ')

    #running subprocess
    process = subprocess.Popen(proc_cmd, stdout=subprocess.PIPE)

    #printing the output from stdout and stop as soon as process ends
    for line in iter(process.stdout.readline, ""):
        line = line.decode()
        proc_running = process.poll() is None
        if not proc_running:
            break

        print("[ZAP]", line[:-1])

    #checking for presence of testreport
    if os.path.exists('testreport.html'):
        print("[LOG] Test report generated successfully")
    else:
        print("[ERR] Test report generation failed")

    #getting the source address from .env
    fromaddr = os.getenv("FROMADDR")

    #getting applicaton specific password of source address
    email_pass= getpass.getpass(prompt='Enter password ')
    
    #input destination address
    toaddr =input("Enter Destination email address: ")

    

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

    #removing reports from the os
    os.remove('testreport.html')
    os.remove('zap.yaml')

    time.sleep(2)

    #removing docker exited docker containers
    cmd2 = f'docker container prune -f'

    proc_cmd2 = cmd2.split(' ')

    subprocess.Popen(proc_cmd2, stdout=subprocess.PIPE)

    print("[LOG] Destroyed Exited containers")

    time.sleep(2)

if __name__ == "__main__":
    main()
