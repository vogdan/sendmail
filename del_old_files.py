#!/usr/bin/env python

#
# Delete all old files in the subdirs of a dir except 
# the ones in a specified dir
#

import time
import os

from argparse import ArgumentParser
from logger import log


def parse_cli_opts():
    arg_parser = ArgumentParser(description='''
Delete old files in the specified dir and it's subdirs, 
excepting the files in the except subdir''')
    arg_parser.add_argument('-a', '--age-limit',
                            help='''File age limit (all files older than AGE days will be deleted)
File age will be determined by time of last access.
''',
                            dest='age',
                            type=int,
                            required=True)
    arg_parser.add_argument('-d', '--parent_dir',
                            help='Parent dir containing all subdirs to delete from',
                            dest='parent',
                            metavar='DIR',
                            required=True)
    arg_parser.add_argument('-e', '--except-subdir',
                            help='Skip files in the specified subdir',
                            metavar='SUBDIR')
    return  arg_parser.parse_args()


def is_old(file, limit):
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
    
    limit_days_ago = time.time() - limit * 24 * 60 * 60
    file_age = os.stat(file).st_mtime
    print'### {}'.format(file)
    print 'limit {}'.format(limit_days_ago)
    print 'age   {}'.format(file_age)
    print 'age_d {}'.format((time.time()-file_age)/(24 * 60 * 60))
    if file_age < limit_days_ago:
        return True
    return False
    


def main():
    args = parse_cli_opts()

    print is_old("/home/bogdan/New Text Document.txt", 10);
    print is_old("/home/bogdan/test.py", 10);

if __name__ == "__main__":
    main()
