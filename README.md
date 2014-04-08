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
      -sig SIGNATURE, --signature SIGNATURE
                            Text file containing signature

```


###del_old_files.py

Delete old files in the specified dir and it's subdirs, excluding the files in
the except subdir

#####Usage

```
        del_old_files.py [-h] -a AGE -d DIR [-e SUBDIR]

        optional arguments:
          -h, --help            show this help message and exit
          -a AGE, --age-limit AGE
                                File age limit (all files older than AGE days will be
                                deleted) File age will be determined by time of most
                                recent content modification.
          -d DIR, --parent_dir DIR
                                Absolute path of parent dir containing all subdirs to
                                delete from
          -e SUBDIR, --except-subdir SUBDIR
                                Skip files in the specified subdir. Relative path
                                inside parent dir
```



###Notes
For each of the abou scripts, an error log file (```mailsend_py.log``` or ```del_old_files_py.log```) will be created in the CWD. 
All errot and information messages will be written to this log and nothing will be displayed at the console, unless the program fails miserably :).
