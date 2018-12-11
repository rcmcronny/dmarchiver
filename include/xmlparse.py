#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from datetime import datetime

class DMARCReport():

	def __init__(self):
		self.submitorg          = ""
		self.submitmail         = ""
		self.repid              = ""
		self.begindate          = ""
		self.enddate            = ""
		self.policy_pub         = {}
		self.policy_eval        = {}
		self.identifiers	= {}
		self.auth_results	= {}
		self.record	        = {}


def parseXMLfromFile(xmlfile):
	DMARC = DMARCReport()
	tree = ET.parse(xmlfile)
	root = tree.getroot()

	for child in root:
		if(child.tag == "report_metadata"):
			for sub in child:
				if(sub.tag == "org_name"):
					DMARC.submitorg = sub.text
				elif(sub.tag == "email"):
					DMARC.submitmail = sub.text
				elif(sub.tag == "report_id"):
					DMARC.repid = sub.text
				elif(sub.tag == "date_range"):
					for key in sub:
						if(key.tag == "begin"):
							DMARC.begindate = key.text
						elif(key.tag == "end"):
							DMARC.enddate = key.text
		elif(child.tag == "policy_published"):
			for sub in child:
				if(sub.tag == "domain"):
					DMARC.policy_pub.update( {'repdomain' : sub.text } )
				elif(sub.tag == "adkim"):
					DMARC.policy_pub.update( {'adkim' : sub.text } )
				elif(sub.tag == "aspf"):
					DMARC.policy_pub.update( {'aspf' : sub.text  } )
				elif(sub.tag == "p"):
					DMARC.policy_pub.update( {'p': sub.text } )
				elif(sub.tag == "pct"):
					DMARC.policy_pub.update( {'pct': sub.text } )

		elif(child.tag == "record"):
			for sub in child:
				if(sub.tag == "row"):
					for key in sub:
						if(key.tag == "source_ip"):
							DMARC.record.update( {'source_ip' : key.text})
						if(key.tag == "count"):
							DMARC.record.update( {'count' : key.text})
						if(key.tag == "policy_evaluated"):
							for tag in key:
								if(tag.tag == "disposition"):
									DMARC.policy_eval.update( {'disposition' : tag.text} )
								if(tag.tag == "dkim"):
									DMARC.policy_eval.update( {'dkim' : tag.text} )
								if(tag.tag == "spf"):
									DMARC.policy_eval.update( {'spf' : tag.text} )

						DMARC.record.update( {'policy_eval': DMARC.policy_eval} )

				elif(sub.tag == "identifiers"):
					for key in sub:
						if(key.tag == "header_from"):
							DMARC.identifiers.update( {'header_from' : key.text})
					DMARC.record.update( {'identifiers': DMARC.identifiers} )

				elif(sub.tag == "auth_results"):
					for key in sub:
						if(key.tag == "dkim"):
							dkim = {}
							DMARC.auth_results.update( {'dkim' : dkim} )

							for tag in key:
								if(tag.tag == "domain"):
									dkim.update( {'domain' : tag.text} )
									DMARC.auth_results.update(dkim)
								elif(tag.tag == "result"):
									dkim.update( {'result' : tag.text} )
									DMARC.auth_results.update(dkim)
								elif(tag.tag == "selector"):
									dkim.update( {'selector' : tag.text} )
									DMARC.auth_results.update(dkim)
						if(key.tag == "spf"):
							spf = {}
							DMARC.auth_results.update( {'spf' : spf} )

							for tag in key:
								if(tag.tag == "domain"):
									spf.update( {'domain' : tag.text } )
									DMARC.auth_results.update(spf)
								elif(tag.tag == "result"):
									spf.update( {'result' : tag.text} )
									DMARC.auth_results.update(spf)
					DMARC.record.update( {'auth_results': DMARC.auth_results} )

	return(DMARC)




current_report = parseXMLfromFile("g.xml")


#print(current_report.submitorg)
#print(current_report.submitmail)
#print(current_report.repdomain)
#print(current_report.repid)
#print(current_report.begindate)
#print(current_report.enddate)

#print(datetime.utcfromtimestamp(int(current_report.begindate)).strftime('%Y-%m-%d %H:%M:%S'))
#print(datetime.utcfromtimestamp(int(current_report.enddate)).strftime('%Y-%m-%d %H:%M:%S'))

print(current_report.record)




