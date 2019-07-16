#-----------------------------------
### Updating sqlite DB with record
### data
#-----------------------------------

import os
import sqlite3
import sys

#-----------------------------------
### 'Inline DB schema'
### (in case DB does not exist ->
### then create it
#-----------------------------------

if(!os.path.isfile(sqlitefile)):
	conn = sqlite3.connect(sqlitefile)
	c = conn.cursor()
	c.execute('''CREATE TABLE dmarc_reports (
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
	)''')
	
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
