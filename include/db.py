#-----------------------------------
### Updating sqlite DB with record
### data
#-----------------------------------

import os
import sqlite3
import sys
	
def connect_db(sqlitefile):
	try:
		conn = sqlite3.connect(sqlitefile)
		return conn
	except Exception as e:
		print("Error creating DB connection:", e)
		sys.exit(1)
		
def get_last_row_id(conn):
	
	sql = '''SELECT ID FROM dmarc_reports ORDER BY ID DESC LIMIT 1;'''
	
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()
	result = cur.fetchall()
	
	for r in result:
		return r
		
def insert_data(conn, values):
	
	sql = '''INSERT INTO dmarc_reports(ID, org_name, org_mail, report_id, begin_date, end_date, pub_domain, pub_adkim, pub_aspf, pub_p, pub_sp, pub_pct, pub_fo, sip, count, eval_disp, eval_dkim,eval_spf, header_from, auth_dkim_dom, auth_dkim_res, auth_spf_dom, auth_spf_res)
			  VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
			  
	cur = conn.cursor()
	cur.execute(sql, values)
	conn.commit()
	
	return cur.lastrowid
