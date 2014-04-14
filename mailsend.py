#!/usr/bin/env python

#
# Send email via Gmail SMTP
#
# Usage info:
#
#        ./mailsend.py -h
#
# 

import smtplib
import re
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from logger import log
from time import gmtime, strftime

GMAIL_USER = 'your gmail user'
GMAIL_PASS = 'your gmail pass'
FROM_ADDR = 'your_username@gmail.com'

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def parse_cli_opts():
    arg_parser = ArgumentParser(description='Send email via Gmail SMTP',
                                formatter_class=RawTextHelpFormatter)
    arg_parser.add_argument('-to', '--to',
                            help='''Message recipient(s). 
Accepted values: * email address;
                 * multiple email addresses separated by ',';
                 * a file containing email addresses, one on each line.''',
                            metavar='RECIPIENT(S)',
                            required=True)
    arg_parser.add_argument('-s', '--subject',
                        help='Message subject.')    
    arg_parser.add_argument('-b', '--body',
                            help='Text file containing message body')
    arg_parser.add_argument('-R', '--rotate',
                            help='''Text file containing subjects and message bodies. 
The script would send the first subject/body for 
the first time it's triggered, the second subject/body 
the next time, etc.

Accepted file structure:

[]
[SUBJECT]
Some Subject
[BODY]
Some body (can be multiline)
---
[X]
[SUBJECT]
Some other subject
[BODY]
Some other body (can be multiline)
---

...


The script will cycle through pairs of subjects and bodies. 
"[X]" marks the pair to start from.''',
                             metavar='TXT_FILE')
    arg_parser.add_argument('-sig', '--signature',
                            help='Text file containing signature')
    return  arg_parser.parse_args()


def read_sbody_from_file(infile):
    # get subject and body
    log.info("Reading subject and body from file: {}".format(infile))
    with open(infile, 'r') as f:
        buff = f.read()
    all_pattern = '(\[X?\])\n*?\[SUBJECT\]((\n.*?)+)\[BODY]((\s.*?)+)---'
    all_p = re.compile(all_pattern, re.IGNORECASE)
    match_list = all_p.findall(buff)
    good_match = None
    if match_list:
        for match in match_list:
            # try to find a section marked as active and use that 
            if '[X]' in match[0] or '[x]' in match[0] :
                good_match = match
                good_match_index = match_list.index(match) 
            # no section marked as active - use first section
            if not good_match:
                good_match = match_list[0]
                good_match_index = -1

        subject = good_match[1]
        body = good_match[3]
        log.info("\tSubject: {}".format(subject))
        log.info("\tBody: {}".format(body))

        # set next section as active
        with open(infile, 'r') as f:
            lines = f.readlines()

        mark_next_active = False
        x_marks_spot = '[X]\n'
        with open(infile, 'w+') as f:
            # if last section was used, mark first as next
            if good_match_index == len(match_list)-1:
                next_not_marked = True
                for line in lines:
                    if '[]' in line and next_not_marked:
                        line = x_marks_spot
                        next_not_marked = False
                    elif '[X]' in line or '[x]' in line:
                        line = '[]\n'
                    f.write(line)
            # if no section was marked as next, and first was used,
            # mark second as next
            elif good_match_index == -1:
                bracket_occurence = 0
                for line in lines:
                    if '[]' in line:
                        if bracket_occurence == 1:
                            line = x_marks_spot
                        bracket_occurence += 1
                    f.write(line)
            # if we had a section marked as next mark the next one 
            else:
                for line in lines:
                    if mark_next_active and '[]' in line:
                        line = x_marks_spot
                        mark_next_active = False
                    elif '[X]' in line or '[x]' in line:
                        line = '[]\n'
                        mark_next_active = True
                    f.write(line)
    else:
        log.info("ERROR: Could not find expected format in subject/body file".format(match_list))
        subject, body = None, None
                 
    return subject, body
    

def main():
    args = parse_cli_opts()

    if not args.body and not args.rotate:
        log.debug("ERROR: A body must be specified using -b or -R")
        exit(1)
    if not args.subject and not args.rotate:
        log.debug("ERROR: A subject must be specified using -s or -R")
        exit(1)

    try:
        # read email addresses from a file if a file is specified
        try:
            with open(args.to, 'rb') as f:
                to_list = f.read().splitlines()
            log.info('Reading recipients from file {}'.format(args.to))
            to = ', '.join(to_list)
        except Exception as e:
            # f is not a file
            to_list  = args.to.split(',')
            to = args.to
            log.info(e)
            log.info("\t\t==> treating '-to' argument as one email address or a list of them...")

        # get subject and body
        if args.rotate:
            subject, body = read_sbody_from_file(args.rotate)
        else:
            subject, body_file = args.subject, args.body
            # add message body
            with open(body_file, 'rb') as f:
                body = f.read()

        # create message
        msg = MIMEMultipart()
        msg['From'] = FROM_ADDR
        msg['To'] = to
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))

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
    mail_errors = main()
    if mail_errors:
        log.debug("SEND ERRORS DETECTED:")
        for key in mail_errors:
            log.debug('\tERROR {}: {}'.format(key, mail_errors[key]))

