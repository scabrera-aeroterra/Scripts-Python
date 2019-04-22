import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

send_from = "soporte@aeroterra.com"
send_to = "scabrera@aeroterra.com"
subject = "Prueba"
text = "Hola\nQue tal?"

server="smtp.office365.com"
port=587

username="scabrera@aeroterra.com"
password="vpwzprqqhtfdrbbf"

msg = MIMEMultipart('related')
msg['From'] = send_from
msg['To'] = send_to if isinstance(send_to, basestring) else COMMASPACE.join(send_to)
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = subject
msg.attach( MIMEText(text,'plain') )

smtp = smtplib.SMTP(server, int(port))
smtp.starttls()
smtp.login(username, password)
smtp.sendmail(send_from, send_to, msg.as_string())
smtp.close()