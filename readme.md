# OWASP-ZAP-Baseline  Automation

->We pulled the docker stable version image using command - 
```powershell
docker pull owasp/zap2docker-stable.
```
->We proceed to take input for the target website and store and run the following docker command as a python subprocess :-
```powershell
docker run -v {cwd_path}:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t {target_site} -r testreport.html
```
->to see the output we must read the output of the running subprocess via stdout and stop as soon as the subprocess stops.

->the generated report is stored in the os which is then sent over to the destination email specified by the user after entering the secure password for source email address which is authenticated.

->smtplib is used to provide a smtp protocol for sending the mail and MIMEmultitext, MIMEmultipart, MIMEbase were used the vivid description is given below:-
```powershell
MIMEBase is just a base class. As the specification says: "Ordinarily you won’t create instances specifically of MIMEBase"
MIMEText is for text (e.g. text/plain or text/html), if the whole message is in text format, or if a part of it is.
MIMEMultipart is for saying "I have more than one part", and then listing the parts - you do that if you have attachments, you also do it to provide alternative versions of the same content (e.g. a plain text version plus an HTML version)
```
->Finally we are destroyed the testreport.html, ZAP.yaml files from the host os and the exited container from docker as well.

commmand to prune(destroy) the exited container was run in a similar way as the ZAP baseline command:-
```powershell
docker container prune -f
```
->The script is provided with comments at each step to enhance readability.
