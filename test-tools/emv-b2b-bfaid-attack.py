#!/usr/bin/python

from emv import *
import sys
import time

def check_aid(aid):
	for plus in range(0x00,0xff+1):
		current_aid = aid + [plus]

		apdu_res = emv.SELECT_AID(current_aid)

		sys.stdout.write("\r\033[KCHECK      : {0:s}".format(map(hex,current_aid)))
		sys.stdout.flush()

		if (apdu_res.sw1 == 0x90):
			tlv=EMV_TLV(apdu_res.data)
			final_aid = tlv.list_childs(0x6f)[0].list_childs(0x84)[0].data
			if (final_aid == current_aid):
				sys.stdout.write(" (FOUND!)\n".format(map(hex,current_aid)))
				tlv.show()
				check_aid(current_aid)
			else:
				check_aid(current_aid)



emv = EMV()

check_aid([])
