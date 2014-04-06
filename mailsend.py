#!/usr/bin/env python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from argparse import ArgumentParser
from logger import log
from time import gmtime, strftime

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
                            help='''Message recipient(s). 
Accepted values: * email address;
                 * multiple email addresses separated by ',';
                 * a file containing email addresses, one on each line.
''',
                            required=True)
    arg_parser.add_argument('-b', '--body',
                            help='Text file containing message body',
                            required=True)
    arg_parser.add_argument('-sig', '--signature',
                            help='Text file containing signature')
    return  arg_parser.parse_args()



def main():
    args = parse_cli_opts()

    try:
        # read email addresses from a file if a file is specified
        try:
            with open(args.to, 'rb') as f:
                to_list = f.read().splitlines()
            log.info('Read recipients from file {}'.format(args.to))
            to = ', '.join(to_list)
        except Exception as e:
            # f is not a file
            to_list  = args.to.split(',')
            to = args.to
            log.info(e)
            log.info("\t\t==> treating '-to' argument as one email address or a list of them...")
    
        # create message
        msg = MIMEMultipart()
        msg['From'] = FROM_ADDR
        msg['To'] = to
        msg['Subject'] = args.subject
        
        # add message body
        with open(args.body, 'rb') as f:
            body_text = f.read()
        msg.attach(MIMEText(body_text, 'plain'))

        # add signature if specified
        if args.signature:
            with open(args.signature, 'rb') as f:
                signature = f.read()
            signature = "\n\n" + signature
            msg.attach(MIMEText(signature, 'plain'))

        # send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        return  server.sendmail(FROM_ADDR, to_list, msg.as_string())
    
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    log_delimiter = "#"*20 + strftime("%a, %d %b %Y %X +0000", gmtime()) + "#"*10
    log.debug("\n"*2 + log_delimiter + "\n") 
    errors = main()
    if errors:
        log.debug("SEND ERRORS DETECTED:")
        for key in errors:
            log.debug('\tERROR {}: {}'.format(key, errors[key]))

