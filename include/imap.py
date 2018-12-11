#-----------------------------------
### Fetching and decompressing
### DMARC report attachments
#-----------------------------------

from imaplib import IMAP4
import email
import re,sys
import yaml

### Config

config = "dmarchiver.conf"

try:
 with open("config", 'r') as ymlfile:
 cfg = yaml.load(ymlfile)
 
 imap_host       = cfg['imap']['scheme']
 imap_port       = cfg['imap']['ipamURL']
 imap_user       = cfg['imap']['apiPath']
 imap_pass       = cfg['imap']['user']
 imap_folder     = cfg['imap']['db']
 done_folder     = cfg['imap']['dbuser']
 use_tls         = cfg['connection']['use_tls']
 use_starttls    = cfg['connection']['use_starttls']
 allowed_content = cfg['content']['allowed']
 daemon_mode	 = cfg['process']['daemon']
 delay_interval  = cfg['process']['delay']
 
except Exception as e:
 print("Error: %s" % (e))
 sys.exit(1)
		
if( (use_tls == True) and (use_starttls == True):
   print("'use_tls' and 'use_starttls' are mutually exclusive, please update your configuration")
   sys.exit(1)

with IMAP4(imap_host, imap_port) as M:
	M.debug = 3

	if(use_starttls == True):
		M.starttls
	elif(use_tls == True):
		#M.ssl
		pass
	else:
		pass

#	M.starttls()
	M.login(imap_user, imap_pass)

	try:
		ret = M.select(done_folder)[0]
		if(ret == 'NO'):
			print("Creating Folder " + done_folder + " ...")
			M.create(done_folder)
	except:
		pass

	M.select(imap_folder)

	typ, msgnums = M.search(None, 'ALL')
	print(typ, msgnums)

	for num in msgnums[0].split():

		typ, data = M.fetch(num, '(BODY[HEADER.FIELDS (DATE)])')
		line = (str(data[0][1]))

		date		= 	re.search("Date:\s(\w*,?\s*\w*\s*\w*\s*\w*\s*\w*:\w*:\w*)", line)
		if(date is not None):
			print(date.group(1))

		typ, data = M.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT)])')
		line = (str(data[0][1]))

		submitter     =	re.search("Submitter:\s(\w*\.\w*)", line)
		if(submitter is not None):
			print(submitter.group(1))

		report_id     =	re.search("Report-ID:\s(<?\w*\.?\w*>?)", line)
		if(report_id is not None):
			print(report_id.group(1))

		report_domain     =	re.search("Report domain:\s(\w*\.\w*)", line)
		if(report_domain is not None):
			print(report_domain.group(1))

		typ, data = M.fetch(num, '(RFC822)')
		print(data[0][1])

		mail = email.message_from_string(data[0][1].decode())
		if(mail.is_multipart()):
			print("MULTI")
			for part in mail.walk():
				ctype = part.get_content_type()
				print(ctype)
				if(ctype in allowed_content):
					open(part.get_filename(), 'wb').write(part.get_payload(decode=True))

		#M.copy(num, done_folder)
		#M.store(num, '+FLAGS', '\\Deleted')



	M.close()
	M.logout()
