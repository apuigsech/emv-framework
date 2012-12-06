#!/usr/bin/python

from emv import *
import sys

emv = EMV()
apdu_res = emv.SELECT_AID([0x32,0x50,0x41,0x59,0x2e,0x53,0x59,0x53,0x2e,0x44,0x44,0x46,0x30,0x31])

if (apdu_res.sw1 != 0x90):
	sys.exit()

tlv = TLV(apdu_res.data)
apdu_res = emv.SELECT_AID(tlv.list_childs(0x6f)[0].list_childs(0xa5)[0].list_childs(0xbf0c)[0].list_childs(0x61)[0].list_childs(0x4f)[0].data)

tlv = TLV(apdu_res.data)
tlv.show()
