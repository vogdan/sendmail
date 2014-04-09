#!/bin/bash

LOAD_DETAILS="details.txt"
MAIL_BODY="mail_body.txt"
HOST=`hostname`

df --total > $LOAD_DETAILS
TOTAL_LOAD=`cat $LOAD_DETAILS | awk 'END{print $5}' | cut -d'%' -f1`

if [ $TOTAL_LOAD -gt 90 ]; then 
    echo "Total load for system '`hostname`' is $TOTAL_LOAD%." > $MAIL_BODY
    echo "" >> $MAIL_BODY
    cat $LOAD_DETAILS >> $MAIL_BODY
    ./mailsend.py -s "System Load Alert" -to "dbogdan@gmail.com" -b $MAIL_BODY
fi
