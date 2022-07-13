#Authors : Mohit Raj, Shomik Ghosh

from json import load
import subprocess
import os
import re

import time

import utilitymodule
from dotenv import load_dotenv
load_dotenv()


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


#getting current working directory path
cwd_path = os.getcwd()

#getting target site input

target_site = input("Enter Target Site: ")
   # Regular expression for URL
re_exp = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" +
            "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")
exp = re.compile(re_exp)
if (target_site == None):
    print("Input string is empty")
if(re.search(exp, target_site)):
    print("Initiating Scan !")
else:
    print("Input URL is invalid!")
    quit()
    


def testreport():
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

def sendmail():

    utilitymodule.sendmail(target_site)
    

def removedocs():

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
    testreport()
    sendmail()
    removedocs()
