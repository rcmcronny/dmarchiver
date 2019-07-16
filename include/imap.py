#-----------------------------------
### Fetching and decompressing
### DMARC report attachments
#-----------------------------------

import email
import sys, re
from imaplib import IMAP4
from include import function
from include import decompress

def fetch_report_imap(imap_host, imap_port, imap_user, imap_pass, imap_folder, done_folder, use_starttls, use_tls):

	skip = False

	if( (use_tls == True) and (use_starttls == True) ):
		print("'use_tls' and 'use_starttls' are mutually exclusive, please update your configuration")
		sys.exit(1)

	try:
		M = IMAP4(imap_host, imap_port)
		#M.debug = 3

		if(use_starttls == True):
			M.starttls()
		elif(use_tls == True):
			#M.ssl
			pass
		else:
			pass

	except Exception as e:
		print("Error: %s" % (e))
		function.log(logfile,"ERR", "Error connecting to IMAP host: %s %s" % (imap_host, e))
		sys.exit(1)

	try:
		M.login(imap_user, imap_pass)

	except Exception as e:
		print("Error authenticating against IMAP host: %s %s" % (imap_host, e))
		function.log(logfile,"ERR", "Error authenticating against IMAP host: %s %s" % (imap_host, e))
		M.close()
		sys.exit(1)

	try:
		ret = M.select(done_folder)[0]
		if(ret == 'NO'):
			print("Creating Folder " + done_folder + " ...")
			M.create(done_folder)
	except:
		pass

	M.select(imap_folder)

	typ, msgnums = M.search(None, 'ALL')
	#print(typ, msgnums)

	for num in msgnums[0].split():

		typ, data = M.fetch(num, '(BODY[HEADER.FIELDS (DATE)])')
		line = (str(data[0][1]))

		date		= 	re.search("Date:\s(\w*,?\s*\w*\s*\w*\s*\w*\s*\w*:\w*:\w*)", line)
		if(date is not None):
			if(debug == True):
				print(date.group(1))

		typ, data = M.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT)])')
		line = (str(data[0][1]))

		submitter     =	re.search("Submitter:\s(\w*\.\w*)", line)
		if(submitter is not None):
			if(debug == True):
				print(submitter.group(1))

		report_id     =	re.search("Report-ID:\s(<?\w*\.?\w*>?)", line)
		if(report_id is not None):
			if(debug == True):
				print(report_id.group(1))

		report_domain     =	re.search("Report domain:\s(\w*\.\w*)", line)
		if(report_domain is not None):
			if(debug == True):
				print(report_domain.group(1))

		typ, data = M.fetch(num, '(RFC822)')
		if(debug == True):
			print(data[0][1])

		mail = email.message_from_string(data[0][1].decode())
		#if(mail.is_multipart()):
		for part in mail.walk():
			ctype = part.get_content_type()
			if(ctype in allowed_content):
				if(part.get_filename() is None):
					continue
				fn = tmpdir + "/" + part.get_filename()
				open(fn, 'wb').write(part.get_payload(decode=True))
			else:
				#Not in allowed content, skip
				skip = True

		if(skip is not False):
			decompress.compr_type(fn)

		M.copy(num, done_folder)
		M.store(num, '+FLAGS', '\\Deleted')

	M.close()
	M.logout()
