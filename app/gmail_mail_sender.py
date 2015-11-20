__author__ = 'matyas'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText
import os

class GmailMessageCreator(object):

    def __init__(self, recipient, subject, message):
        self.email_from_adress = '.....'
        self.email_from_pwd = '.....'

        self.recipient = recipient
        self.subject = subject
        self.message = message

        self.msg = MIMEMultipart()
        self.msg['From'] = self.email_from_adress
        self.msg['To'] = recipient
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(message))

    def send_mail(self):
        try:
            mailserver = smtplib.SMTP('smtp.gmail.com', 587)
            # identify ourselves to smtp gmail client
            mailserver.ehlo()
            # secure our email with tls encryption
            mailserver.starttls()
            # re-identify ourselves as an encrypted connection
            mailserver.ehlo()
            mailserver.login(self.email_from_adress, self.email_from_pwd)
            mailserver.sendmail(self.email_from_adress, self.recipient, self.msg.as_string())
            mailserver.quit()
        except Exception as e:
            print 'something went wrong while I was trying to deliver the following message : %s to %s' % (
                self.message, self.recipient), e