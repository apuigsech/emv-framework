#!/usr/bin/python

from emv import *
import sys

emv = EMV()
apdu_res = emv.SELECT_AID([0xa0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10])

if (apdu_res.sw1 == 0x90):
	tlv = EMV_TLV(apdu_res.data)
	tlv.show()

print '================================================================\n\n'

for i in range(1,32):
	for j in range(1,255):
		sys.stdout.write('\r\033[KCHECK      : {0:x} {1:x}'.format(i, j))
		sys.stdout.flush()
		apdu_res = emv.READ_RECORD(i, j)
		if (apdu_res.sw1 == 0x90):
			sys.stdout.write(" (FOUND!)\n")
			print '----------------------------------------------------------------'
			tlv = EMV_TLV(apdu_res.data)
			tlv.show()
			print '----------------------------------------------------------------\n\n\n'
