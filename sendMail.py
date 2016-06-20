# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def senMail(to, info):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    #Next, log in to the server
    server.login("webcoreconsulting@gmail.com", "QA5-as3-MVU-5LW")
    html2 = """\
    <html>
    <head><meta charset="UTF-8"></head>
    <body>
    <h1>Daglig rapport</h1>
    """
    for i in info:
        html2 += "<div>" \
                 "<h3>"+i[2]+" - "+i[3]+" </h3>" \
                 "<p>"+i[1]+"</p>" \
                 "<p><b>Beskrivelse:</b></p>"\
                 "<p>"+i[0]+"</p>"\
                 "<p><b>Bruker:</b></p>"\
                 "<p>"+i[4]+"</p>"\
                 "</div><br>"

    html2 += """</body></html>"""

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Daglig rapport"
    msg['From'] = 'webcoreconsulting@gmail.com'
    msg['To'] = to

    part2 = MIMEText(html2.encode('utf-8'), 'html', 'utf-8')
    msg.attach(part2)
    server.sendmail('webcoreconsulting@gmail.com', to, msg.as_string())
    server.quit()

