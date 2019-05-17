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

# DB schema

	CREATE TABLE dmarc_reports (
		ID INT PRIMARY KEY NOT NULL,
		org_name CHAR(50) NOT NULL,
		org_mail CHAR(80) NOT NULL,
		report_id CHAR(50) NOT NULL UNIQUE,
		begin_date INT NOT NULL,
		end_date INT NOT NULL,
		pub_domain CHAR(80) NOT NULL,
		pub_adkim CHAR(2) NOT NULL,
		pub_aspf CHAR(2) NOT NULL,
		pub_p CHAR(20) NOT NULL,
		pub_sp CHAR(20) NOT NULL,
		pub_pct INT NOT NULL,
		pub_fo  INT NOT NULL,
		sip CHAR(18) NOT NULL,
		count INT NOT NULL,
		eval_disp CHAR(10) NOT NULL,
		eval_dkim CHAR(10) NOT NULL,
		eval_spf CHAR(10) NOT NULL,
		header_from CHAR(50) NOT NULL,
		auth_dkim_dom CHAR(50) NOT NULL,
		auth_dkim_res CHAR(10) NOT NULL,
		auth_spf_dom CHAR(50) NOT NULL,
		auth_spf_res CHAR(10) NOT NULL
	);


# web statistics

Please note: dmarchiver uses Chart.js to generate and display dmarchiver's statistics.
