zevtools
========


#### mailsend.py

Send email via Gmail SMTP


#####USAGE

```
    mailsend.py [-h] -s SUBJECT -to TO -b BODY

    Send email via Gmail SMTP

    Arguments:
      -h, --help            show this help message and exit
      -s SUBJECT, --subject SUBJECT
                            Message subject
      -to TO, --to TO       Message recipient(s). 
                            Accepted values: 
                               * email address; 
                               * multiple email addresses separated by ',';
                               * a file containing email addresses, one on each line.

      -b BODY, --body BODY  Text file containing message body
      -sig SIGNATURE, --signature SIGNATURE
                            Text file containing signature

```

#####Notes

An error log file named ```mailsend_py.log``` is created and located in the CWD. 
All messages will be written to this log and nothing will be displayed at the console, unless the program fails miserably :).
