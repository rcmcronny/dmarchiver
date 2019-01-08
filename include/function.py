#-----------------------------------
### Some helper functions
#-----------------------------------

import sys
from datetime import datetime

def log(logfile,severity, message):
	if(severity == "WARN"):
		prefix = "[WARN]"
	elif(severity == "ERR"):
		prefix = "[ERR]"
	elif(severity == "INFO"):
		prefix = "[INFO]"
	else:
		pass

	cur_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	try:
		with open(logfile, 'a') as logf:
			logf.write(prefix + "[" + cur_date + "]: " + message + "\n")

	except Exception as e:
		print("Error opening %s: %s\n" % (logfile,e))
		sys.exit(1)
