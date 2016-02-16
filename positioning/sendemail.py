import smtplib, os, time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
me = "rsteinpython@gmail.com"
you = "rstein_codealerts@outlook.com"
you = me

def send(codename, message=None, text=True):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Python Code Update - " + codename
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Congratulations!\nYour Python Code " + codename + " has finished running!\n Now go and do somthing else."
    html = """\
    <html>
    <head></head>
        <body>
            <p>Congratulations!<br>
            Your Python script,  """ + codename + """,  has finished running!<br>
            Now go and do somthing else.
            </p>
            <p> Additional Information...<br>
            """ + str(message) + """</p>
        </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('rsteinpython@gmail.com', 'pythonscripts')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()
    
    if text:
		print time.asctime(time.localtime()), "Email notification sent to", you


#INCLUDE AT THE END OF A SCRIPT WITH CUSTOMISED MESSAGE 
#Sends an email notification

#message = str(time.asctime(time.localtime())) + " Created new tree at /net/storage03/data/users/rstein/tuples/pid/" + tupleName+ ".root"
#print message
#
#import os, sys
#sys.path.append('/home/rstein/pythonscripts/misc')
#import sendemail as se
#name = os.path.basename(__file__)
#se.send(name, message)
