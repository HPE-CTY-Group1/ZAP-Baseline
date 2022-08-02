# OWASP-ZAP-Baseline  Automation

## Getting Started

This is repository is for demonstration of Automated framework for ZAP baseline scan using the docker instance of ZAP to crawl the target site, sending the generated report to given destination email id and removing it form the host os.

### Prerequisites

* docker
  ```sh
   docker pull owasp/zap2docker-stable.
  ```

### Installation

To run the scan follow the steps:

1. Clone the repo
   ```sh
   git clone https://github.com/HPE-CTY-Group1/ZAP-Baseline.git
   ```
2.Add env file
   ```sh
   FROMADDR="testmohit2727@yahoo.com"
   ```
3. Run the docker image owasp/zap2docker-stable
4. Use sample password for smtpl

### Things our project does

1.We take the target_website which we want to scan and run docker container as python subprocess.
2.We check for invalid input through regex for all the input site.
3.We display the subprocess output and stop as soon as the process stops.
3.Report is generated as testreport.html and store it in os.
4.Generated report is mailed, by taking sender mail id and password.
5.Smtplib is used to provide a Smtp protocol for sending the mail and MIMEmultitext, MIMEmultipart, MIMEbase for attachments.
6.Pruning the docker containers which are executed and stopped.
