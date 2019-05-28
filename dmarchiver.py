#!/usr/bin/env python3

import builtins
import json
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
	fh = open(config, 'r')
except FileNotFoundError:
	try:
		config = os.path.dirname(os.path.realpath(__file__)) + "/dmarchiver.conf"
		fh = open(config, 'r')
	except FileNotFoundError:
		print("No Config file found, Aborting")
		sys.exit(1)
	

try:
	with open(config, 'r') as ymlfile:
		cfg = yaml.safe_load(ymlfile)

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
		sqlitefile		= cfg['process']['sqlitefile']
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
builtins.sqlitefile			= sqlitefile



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

for fn in os.listdir(tmpdir):
	
	if  ( fn.endswith(".xml") ):
		abs_fn = os.path.abspath(os.path.join(tmpdir,fn))
		current_report = xmlparse.parseXMLfromFile(abs_fn)
		print(current_report.submitorg)
		print(current_report.submitmail)
		print(current_report.repdomain)
		print(current_report.repid)
		print(current_report.begindate)
		print(current_report.enddate)
		print(datetime.utcfromtimestamp(int(current_report.begindate)).strftime('%Y-%m-%d %H:%M:%S'))
		print(datetime.utcfromtimestamp(int(current_report.enddate)).strftime('%Y-%m-%d %H:%M:%S'))
		#print(current_report.policy_pub)
		#print(current_report.identifiers)
		#print(current_report.auth_results)
				
		data = json.loads(json.dumps(current_report.policy_pub))
		
		repdomain	= data['repdomain']

		try:
			adkim 	= data['adkim']
		except:
			adkim	= "N/A"

		try:
			aspf	= data['aspf']
		except:
			aspf	= "N/A"

		try:
			p		= data['p']
		except:
			p		= "N/A"
			
		try:
			sp		= data['sp']
		except:
			sp		= "N/A"

		try:
			pct		= data['pct']
		except:
			pct		= "N/A"

		try:
			fo		= data['fo']
		except:
			fo		= "N/A"

		data = json.loads(json.dumps(current_report.policy_eval))

		disposition	= data['disposition']
		dkim		= data['dkim']
		spf			= data['spf']
		
		data = json.loads(json.dumps(current_report.identifiers))
		
		header_from	= data['header_from']
		
		data = json.loads(json.dumps(current_report.auth_results))
		
		try:
			auth_dkim_dom	= data['dkim']['domain']
		except:
			auth_dkim_dom	= "N/A"
		
		try:
			auth_dkim_res	= data['dkim']['result']
		except:
			auth_dkim_res	= "N/A"
		
		try:
			auth_spf_dom	= data['spf']['domain']
		except:
			auth_spf_dom	= "N/A"
		
		try:
			auth_spf_res	= data['spf']['result']
		except:
			auth_spf_res	= "N/A"
			
		conn = db.connect_db(sqlitefile)
		ID = db.get_last_row_id(conn)

		if ( ID == None ):
			ID = 1
		else:
			ID = ID[0] + 1
		
		insert_data = (ID, current_report.submitorg, current_report.submitmail, current_report.repid, 
					   current_report.begindate, current_report.enddate, repdomain, adkim, aspf, p, sp, pct,
					   fo, current_report.sip, current_report.cnt, disposition, dkim, spf, header_from,
					   auth_dkim_dom, auth_dkim_res, auth_spf_dom, auth_spf_res );
		
		try:
			db.insert_data(conn, insert_data)
		except Exception as e:
			function.log(logfile, "ERR", str(e)) 
		
		os.remove(abs_fn)
