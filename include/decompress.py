#-----------------------------------
### Decompressing
### DMARC report attachments
#-----------------------------------

import binascii
import gzip, zipfile

def compr_type(filename):
	with open(filename, 'rb') as testfile:
		# GZIP?
		if(binascii.hexlify(testfile.read(2)) == b'1f8b'):
			print("File is gzip compressed")
			newfile = filename.strip('.')[0] + ".xml"
			zf = gzip.open(filename, 'rb')
			content = zf.read()
			with open(newfile, 'wb') as newf:
				newf.write(content)
		# ZIP?
		else:
			if(zipfile.is_zipfile(filename)):
				print("File is zip compressed")
				with zipfile.ZipFile(filename) as zf:
					zf.extractall()
