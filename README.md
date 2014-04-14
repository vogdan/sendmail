zevtools
========



###mailsend.py

Send email via Gmail SMTP


#####Usage

```
    mailsend.py [-h] -s SUBJECT -to TO -b BODY [-sig SIGNATURE]

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
      -R TXT_FILE, --rotate TXT_FILE
                        Text file containing subjects and message bodies. 
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
                        "[X]" marks the pair to start from.

      -sig SIGNATURE, --signature SIGNATURE - optional -
                            Text file containing signature

```



###del_old_files.py

Delete old files in the specified dir and it's subdirs, excluding the files in
the except subdir

#####Usage

```
        del_old_files.py [-h] -a AGE -d DIR [-e SUBDIR]

        Delete files older thatn AGE days in the DIR directory, except the files in the 
        SUBDIR subdirectory.

        Arguments:
          -h, --help            show this help message and exit
          -a AGE, --age-limit AGE
                                File age limit (all files older than AGE days will be
                                deleted) File age will be determined by time of most
                                recent content modification.
          -d DIR, --parent_dir DIR
                                Absolute path of parent dir containing all subdirs to
                                delete from
          -e SUBDIR, --except-subdir SUBDIR - optional -
                                Skip files in the specified subdir. Relative path
                                inside parent dir.
```


###load_alert.sh

Uses ```mailsend.py``` to send email when the system load limit is more than the specified limit.

#####Usage

```
      ./load_alert.sh [-h] -to EMAIL -lim LIMIT
      
      Send email to EMAIL when the host total disk load in more than LIMIT%

      Arguments:
            -h      show this help and exit
            -to     - mandatory arg - email address to send alert message to
            -lim    - mandatory arg - total system disk load limit that will trigger the email sending

      Example:
            ./load_alert.sh -to you@mail.com -lim 90
          Sends mail to you@mail.com when the host total disk load is more than 90%
```


###Notes
For each of the above scripts, a ```.log``` file will be created in the CWD:
 * ```mailsend_py.log``` for ```mailsend.py``` 
 * ```del_old_files_py.log``` for ```del_old_files.py```

All error and information messages will be written to this log and nothing will be displayed at the console, unless the program fails miserably :).
