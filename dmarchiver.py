#!/usr/bin/env python3

import builtins
import os, re,sys
import yaml

from datetime import datetime


### Custom includes

from include import db
from include import decompress
from include import function
from include import imap
from include import xmlparse


### Config

config = "/etc/dmarchiver.conf"

try:
	with open(config, 'r') as ymlfile:
		cfg = yaml.load(ymlfile)

		imap_host       = cfg['imap']['imap_host']
		imap_port       = cfg['imap']['imap_port']
		imap_user       = cfg['imap']['imap_user']
		imap_pass       = cfg['imap']['imap_pass']
		imap_folder     = cfg['imap']['imap_folder']
		done_folder     = cfg['imap']['done_folder']
		use_tls         = cfg['connection']['use_tls']
		use_starttls    = cfg['connection']['use_starttls']
		allowed_content = cfg['content']['allowed']
		daemon_mode		= cfg['process']['daemon']
		delay_interval  = cfg['process']['delay']
		logfile			= cfg['process']['logfile']
		tmpdir			= cfg['process']['tmpdir']
		debug			= cfg['process']['debug']

except Exception as e:
	print("Error: %s" % (e))
	log(logfile,"ERR", "Error parsing config file: %s" % (e))
	sys.exit(1)

### make 'logfile' and 'allowed_content', 'tmpdir' variable global to all imported modules
builtins.logfile 			= logfile
builtins.allowed_content	= allowed_content
builtins.tmpdir				= tmpdir
builtins.debug				= debug



### check if tmpdir exists
if not os.path.exists(tmpdir):
		try:
			function.log(logfile, "INFO", "temp path doesn't exist, trying to create")
			os.makedirs(tmpdir)
		except Exception as e:
			print("Error: %s" % (e))
			sys.exit(1)


### Fetching reports via IMAP
imap.fetch_report_imap(imap_host, imap_port, imap_user, imap_pass, imap_folder, done_folder, use_starttls, use_tls)

### Parsing reports
#current_report = xmlparse.parseXMLfromFile("test.xml")


#print(current_report.submitorg)
#print(current_report.submitmail)
#print(current_report.repdomain)
#print(current_report.repid)
#print(current_report.begindate)
#print(current_report.enddate)

#print(datetime.utcfromtimestamp(int(current_report.begindate)).strftime('%Y-%m-%d %H:%M:%S'))
#print(datetime.utcfromtimestamp(int(current_report.enddate)).strftime('%Y-%m-%d %H:%M:%S'))

#print(current_report.record)
