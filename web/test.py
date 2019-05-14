import sqlite3
import re
from flask import Flask
from flask import render_template

app = Flask(__name__)

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


DATABASE="dmarchiver.sqlite"

@app.route("/")
def hello():

	labels = []
	values = []
	pub_domain = []
	pub_domain_count = []

	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	cur.execute("SELECT org_name, COUNT(*) FROM dmarc_reports GROUP BY org_name")
	conn.commit()

	rows = cur.fetchall();

	for i in rows:
		labels.append(i[0])
		values.append(i[1])

	str_labels = ""
	str_values = ""
	str_pub_domain_count = ""

	for i in values:
		str_values = str(str_values) + str(i) + ","

	cur.execute("SELECT pub_domain, COUNT(*) FROM dmarc_reports GROUP BY pub_domain")
	conn.commit()

	rows = cur.fetchall();

	for i in rows:
		pub_domain.append(i[0])
		pub_domain_count.append(i[1])

	for i in pub_domain_count:
		str_pub_domain_count = str(str_pub_domain_count) + str(i) + ","


	return render_template("test.html",title='DMARC Report Overview', max=100, values=str_values, labels=labels, colors=colors, pub_domain=pub_domain, pub_domain_count=str_pub_domain_count)


@app.route('/alignment')
def algiment():
	return render_template("alignment.html",title='DMARC Alignment Overview', max=100, colors=colors)




#@app.route("/")


