
import sys
import os
import logging

LOG_FILE = "_".join(sys.argv[0].strip("./").split(".")) + ".log"
LOG_FILE_PATH = os.getcwd()

#####################################################
# Logging HOWTO
# 1. Do not use print. Use the log object instead by
# importing it in your .py file:
# from config import log
# 1a. Only use print if you want messages to be displayed
# at the console but not in the log file
# 2. To log message to console and log file use
# log.info(message)
# 3. To log message only to log file (debug messages) use
# log.debug(message)
# 4. Warning (log.warning )and error (log.error) messages
# will be logged to both console and log file.
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
# log to file
fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.DEBUG)
fh_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
fh.setFormatter(fh_format)
log.addHandler(fh)

