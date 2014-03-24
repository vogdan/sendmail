#!/usr/bin/env python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from argparse import ArgumentParser

GMAIL_USER = 'your gmail user'
GMAIL_PASS = 'your gmail pass'
FROM_ADDR = 'your_username@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def parse_cli_opts():
    arg_parser = ArgumentParser(description='''Send email via Gmail SMTP''')
    arg_parser.add_argument('-s', '--subject',
                        help='Message subject',
                        required=True)
    arg_parser.add_argument('-to', '--to',
                            help='Message recipuent',
                            required=True)
    arg_parser.add_argument('-b', '--body',
                            help='Text file containing message body',
                            required=True)
    return  arg_parser.parse_args()

args = parse_cli_opts()
try:

    msg = MIMEMultipart()
    msg['From'] = FROM_ADDR
    msg['To'] = args.to
    msg['Subject'] = args.subject

    with open(args.body, 'rb') as f:
        body_text = f.read()
        msg.attach(MIMEText(body_text, 'plain'))
        
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASS)
    server.sendmail(FROM_ADDR, args.to, msg.as_string())

except Exception as e:
    print "ERROR: EXCEPTION > {}".format(e)

