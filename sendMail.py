import smtplib
from models import *

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
#Next, log in to the server
server.login("webcoreconsulting@gmail.com", "QA5-as3-MVU-5LW")

#Send the mail
msg = "\r\n".join([
  "From: webcoreconsulting@gmail.com",
  "To: espen.gjernes@gmail.com",
  "Subject: test mail",
  "",
  "dette er en mail"
  ])


def senMail():
    server.sendmail("webcoreconsulting@gmail.com", "espen.gjernes@gmail.com", msg)
