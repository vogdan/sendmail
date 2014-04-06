import sys
import os
import logging

LOG_FILE = "_".join(sys.argv[0].strip("./").split(".")) + ".log"
LOG_FILE_PATH = os.getcwd()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
# log to file
fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.DEBUG)
fh_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
fh.setFormatter(fh_format)
log.addHandler(fh)

