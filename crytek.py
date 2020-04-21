
from P4 import P4,P4Exception
from configparser import ConfigParser
from socket import gaierror
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import subprocess
import os
import smtplib
import logging
import sys
import shutil

config = ConfigParser()
config.read("config.ini")
config.sections()

#load the data from the config.ini file
p4username= config.get('perforce', 'P4username')
port= config.get('mailtrap', 'Port')
smtp_server= config.get('mailtrap', 'Smtp_server')
login= config.get('mailtrap', 'Login')
password= config.get('mailtrap', 'Password')


subject = "Build Logs and Changelist"
sender_email= config.get('mailtrap', 'Sender_email')
receiver_email= config.get('mailtrap', 'Receiver_email')


message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

#body of the email alrt that would fired in case of build failure.
body = "Build has failed , please find the attached output logs and changelist"
message.attach(MIMEText(body, "plain"))


output = "output.txt"
changes = "changelist.txt"


subprocess.call(['./pull.sh'])


#check if the required binary is found in the workspace.
exists = os.path.isfile('./workspace/depot/target/jb-hello-world-maven-0.1.0.jar')
if exists:
    #In case the required binary is found transfer the artifact to client workspace and submit to perforce depot.
    os.chdir("./workspace/depot/target")
    print("the file is present")
    shutil.move("jb-hello-world-maven-0.1.0.jar", "/Users/a5900533/Downloads/new java/depot/bin/jb-hello-world-maven-0.1.0.jar")
    os.chdir("Users/a5900533/Downloads/new java/depot/bin") #Moving to the client root workspace in local
    os.system('p4 add *.jar') #marking the jarfile to add
    os.system('p4 submit -f submitunchanged -d "adding the jar file to bin"') #submit to perforce server depot.
    
else:
    # Shoot out a mail to the team in case of build failure using mailtrap smtp server
    os.chdir("./workspace/depot")

    with open(output, "rb") as attachment:
    # The content type "application/octet-stream" means that a MIME attachment is a binary file
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    with open(changes, "rb") as attachment:
    # The content type "application/octet-stream" means that a MIME attachment is a binary file
        tarp = MIMEBase("application", "octet-stream")
        tarp.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {output}",
    )

    tarp.add_header(
        "Content-Disposition",
        f"attachment; filename= {changes}",
    )

    message.attach(part) #message.attach() method for sending attachments to mailtrap smtp server
    text = message.as_string()

    message.attach(tarp)
    text = message.as_string()

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login(login, password)
        server.sendmail(
            sender_email, receiver_email, text
        )
    print('Sent')

 




