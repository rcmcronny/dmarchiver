#-----------------------------------
### Decompressing
### DMARC report attachments
#-----------------------------------

import binascii, os
import gzip, zipfile

def compr_type(filename):
	newfile = os.path.splitext(filename)
	newfile = newfile[0] + ".xml"

	print(newfile)

	with open(filename, 'rb') as testfile:
		# GZIP?
		if(binascii.hexlify(testfile.read(2)) == b'1f8b'):
			print("File is gzip compressed")
			zf = gzip.open(filename, 'rb')
			content = zf.read()
			with open(newfile, 'wb') as newf:
				newf.write(content)
			os.remove(filename)
		# ZIP?
		elif(zipfile.is_zipfile(filename)):
				print("File is zip compressed")
				with zipfile.ZipFile(filename) as zf:
					zf.extractall(tmpdir)
				os.remove(filename)
		else:
			log(ERR, "Unsupported compression method, cannot decompress archive")
			sys.exit(1)
