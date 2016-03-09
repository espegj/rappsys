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
        html2 += "<div style='background-color:#009bd4;border-radius: 5px;padding-top: 5px;padding-right: 5px;padding-bottom: 5px;padding-left: 5px;margin-top: 10px;'>" \
                 "<h3 style='color:white'>"+i[2]+" - "+i[3]+" </h3>" \
                 "<p style='color:white'>"+i[1]+"</p>"\
                 "<p style='color:white'>"+i[0]+"</p>"\
                 "<p style='color:white'>"+i[4]+"</p>"\
                 "</div>"

    html2 += """</body></html>"""

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Daglig rapport"
    msg['From'] = 'webcoreconsulting@gmail.com'
    msg['To'] = to

    part2 = MIMEText(html2.encode('utf-8'), 'html', 'utf-8')
    msg.attach(part2)
    server.sendmail('webcoreconsulting@gmail.com', to, msg.as_string())
    server.quit()

