# OWASP-ZAP Automation
->We ran owasp/zap2docker-stable scan in our docker container.
->We take input for the website we are generating our report,we are using the following docker command:-
```powershell
docker run -v {cwd_path}:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t {target_site} -r testreport.html
```
->Once report is generated we send mail using smtp by attaching the report to target mail address which we take input from the user
->Finally we are destroying the container using the following docker commmand:-
```powershell
docker container prune -f
```