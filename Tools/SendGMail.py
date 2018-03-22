#!/bin/python

import smtplib
import email
import sys
sys.path.append('..')
from Config import Gmail
from time import sleep

def SendMail(mailinfo,targetaddress):
    smtpserver = 'smtp.gmail.com'
    username = Gmail['username']
    password = Gmail['password']
    message = email.Message.Message()
    message['Subject'] = 'WARN'
    message['From'] = Gmail['username']
    message['To'] = targetaddress
    message.set_payload(mailinfo)
    msg = message.as_string()
    sm = smtplib.SMTP(smtpserver, port=587, timeout=20)
    sm.set_debuglevel(0)
    sm.ehlo()
    sm.starttls()
    sm.ehlo()
    sm.login(username, password)
    sm.sendmail(Gmail['username'], targetaddress, msg)
    sleep(5)
    sm.quit()
    return 0