# dmarchiver
A tool for fetching DMARC reports from your INBOX, parsing and archiving

Written in Python.


Requirements

* IMAP capable mail server
* Read and Write permission for your IMAP user
* IMAP Folder where your DMARC reports are stored
* (Sub-)IMAP folder where your processed DMARC reports go
* Local sqlite database (for reporting etc.)

Features

* Supports IMAP connection with STARTTLS / SSL

Future Releases

* web panel for reporting
