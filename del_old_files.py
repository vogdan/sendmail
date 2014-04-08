#!/usr/bin/env python

#
# Delete all old files in the subdirs of a dir except 
# the ones in a specified dir
#

import time
import os

from argparse import ArgumentParser
from logger import log

MIN_SECS = 60
HOUR_SECS = MIN_SECS * 60
DAY_SECS = HOUR_SECS * 24

def parse_cli_opts():
    arg_parser = ArgumentParser(description='''
Delete old files in the specified dir and it's subdirs, 
excluding the files in the except subdir''')
    arg_parser.add_argument('-a', '--age-limit',
                            help='''File age limit (all files older than AGE days will be deleted)
File age will be determined by time of most recent content modification.
''',
                            dest='age',
                            type=int,
                            required=True)
    arg_parser.add_argument('-d', '--parent_dir',
                            help='Absolute path of parent dir containing all subdirs to delete from',
                            dest='parent',
                            metavar='DIR',
                            required=True)
    arg_parser.add_argument('-e', '--except-subdir',
                            help='''Skip files in the specified subdir.
Relative path inside parent dir''',
                            dest = 'exclude',
                            metavar='SUBDIR')
    return  arg_parser.parse_args()


def is_old(fname, limit):
    """
    Check if file is older than limit days

    :type file: str
    :param file: name of file to check (assumes file exists)

    :type limit: int 
    :param limit: maximum file age

    :rtype: boolean
    :return: True - file is older than limit days
             False - otherwise
    """
    limit_secs = limit * DAY_SECS
    limit_days_ago = time.time() - limit_secs
    file_age = get_file_age(fname, 'secs')    
    if file_age < limit_days_ago:
        return True
    return False


def get_file_age(fname, unit='secs'):
    secs_age = time.time() - os.stat(fname).st_mtime
    if unit is 'days':
        divider = DAY_SECS
    elif unit is 'hours':
        divider = HOUR_SECS
    elif unit is 'mins':
        divider = MIN_SECS
    else:
        divider = 1

    return secs_age/divider

        
def main():
    args = parse_cli_opts()

    log.info('''
Deleting all files:
\t-- older than {} days
\t-- in dir {}
\t-- except subdir "{}"'''.format(args.age, args.parent, args.exclude))

    for root, subdirs, files in os.walk(args.parent, topdown=False):
        for name in files:
            full_name = os.path.join(root, name)
            log.info("Deleting: {}".format(full_name))
            if is_old(full_name, args.age):
                if args.exclude and args.exclude in full_name:
                    log.info("Skipping - file in exclude subdir '{}'".format(args.exclude))
                else:
                    os.remove(full_name)
                    log.info("Done.")
            else:
                log.info("Skipping - file not old enough (age: {} days old)".format(
                        get_file_age(fname, 'days')))
            

if __name__ == "__main__":
    log_delimiter = "#"*20 + time.strftime("%a, %d %b %Y %X +0000", 
                                           time.gmtime()) + "#"*10
    log.info("\n"*2 + log_delimiter + "\n") 
    
    try:
        main()
    except Exception, e:
        log.exception(e)

