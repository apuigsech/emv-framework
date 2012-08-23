#!/usr/bin/python

#
#    Python ISO7816 (as part of EMV Framework)
#    Copyrigh 2012 Albert Puigsech Galicia <albert@puigsech.com>
#
#    This code is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnection import CardConnection
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.Exceptions import CardRequestTimeoutException

from tlv import *

INS_DB = (
	{
		'name':'READ_BINARY',
		'code':0xb0
	},
	{
		'name':'WRITE_BINARY',
		'code':0xd0
	},
	{
		'name':'UPDATE_BINARY',
		'code':0xd6
	},
	{
		'name':'ERASE_BINARY',
		'code':0x0e
	},
	{
		'name':'READ_RECORD',
		'code':0xb2
	},
	{
		'name':'WRITE_RECORD',
		'code':0xd2
	},
	{
		'name':'APPEND_RECORD',
		'code':0xe2
	},
	{
		'name':'UPDATE RECORD',
		'code':0xdc
	},
	{
		'name':'GET_DATA',
		'code':0xca
	},
	{
		'name':'PUT_DATA',
		'code':0xda
	},
	{
		'name':'SELECT_FILE',
		'code':0xa4
	},
	{
		'name':'VERIFY',
		'code':0x20
	},
	{
		'name':'INTERNAL_AUTHENTICATE',	
		'code':0x88
	},
	{
		'name':'EXTERNAL AUTHENTICATE',
		'code':0xb2
	},
	{
		'name':'GET_CHALLENGE',
		'code':0xb4
	},
	{
		'name':'MANAGE_CHANNEL',
		'code':0x70
	}
)

TAGS_DB = {}

class ISO7816:
	def __init__(self):
		cardtype = AnyCardType()
		cardrequest = CardRequest(timeout=10, cardType=cardtype)
		self.card = cardrequest.waitforcard()
		self.card.connection.connect()
		self.ins_db = []
		self.ins_db_update(INS_DB)
		self.tags_db = {}
		self.tags_db_update(TAGS_DB)

	def ins_db_update(self, new): 
		self.ins_db += new
	

	def ins_db_resolv(self, name):
		for e in self.ins_db:
			if e['name'] == name:
				return e['code']
		return 0x00

	def tags_db_update(self, new):
		self.tags_db.update(new)


	def send_apdu(self, ins, p1, p2, cla=0x00, data=None, le=None):
		apdu = [cla, ins, p1, p2]
		if data != None:
			apdu += [len(data)] + data
		if le != None:
			apdu += le
		return self.send_apdu_raw(apdu)

	def send_apdu_raw(self, apdu):
		return self.card.connection.transmit(apdu)
		
	def READ_BINARY(self, p1=0x00, p2=0x00, len=0x00):
		ins = self.ins_db_resolv('READ_BINARY')
		self.send_apdu(ins=ins, p1=p1, p2=p2, le=len)
		return

	def WRITE_BINARY(self, p1=0x00, p2=0x00, data=[]):
		ins = self.ins_db_resolv('WRITE_BINARY')
		self.send_apdu(ins=ins, p1=p1, p2=p2, data=data)
		return

	def UPDATE_BINRY(self, p1=0x00, p2=0x00, data=[]):
		ins = self.ins_db_resolv('UPDATE_BINRY')
		self.send_apdu(ins=ins, p1=p1, p2=p2, data=data)
		return

	def ERASE_BINARY(self, p1=0x00, p2=0x00, data=None):
		ins = self.ins_db_resolv('ERASE_BINARY')
		self.send_apdu(ins=ins, p1=p1, p2=p2, data=data)
		return

	def READ_RECORD(self, sfi, record=0x00):
		ins = self.ins_db_resolv('READ_RECORD')
		self.send_apdu(ins=ins, p1=record, p2=(sfi<<3)+4)
		return

	def WRITE_RECORD(self, sfi, data, record=0x00):
		ins = self.ins_db_resolv('WRITE_RECORD')
		self.send_apdu(ins=ins, p1=record, p2=(sfi<<3)+4, data=data)
		return

	def APPEND_RECORD(self, sfi):
		ins = self.ins_db_resolv('APPEND_RECORD')
		self.send_apdu(ins=ins, p1=0x00, p2=(sfi<<3), data=data)
		return

	def UPDATE_RECORD(self, sfi, data, record=0x00):
		ins = self.ins_db_resolv('UPDATE_RECORD')
                self.send_apdu(ins=ins, p1=record, p2=(sfi<<3)+4, data=data)
		return

	def GET_DATA(self, data_id):
		ins = self.ins_db_resolv('GET_DATA')
		self.send_apdu(ins=ins, p1=data_id[0], p2=data_id[1]) 
		return

	def PUT_DATA(self, data_id, data):
		ins = self.ins_db_resolv('PUT_DATA')
		self.send_apdu(ins=ins, p1=data_id[0], p2=data_id[1], data=data)
		return

	def SELECT_FILE(self, data, p1=0x00, p2=0x00):
		ins = self.ins_db_resolv('SELECT_FILE')
		res,sw1,sw2 = self.send_apdu(ins=ins, p1=p1, p2=p2, data=data)
		tlv = TLV(self.tags_db)
		tlv.parse(res)
		return

	def VERIFY(self):
		return

	def INTERNAL_AUTHENTICATE(self):
		return

	def EXTERNAL_AUTHENTICATE(self):
		return

	def GET_CHALLENGE(self):
		return

	def MANAGE_CHANNEL(self):
		return

	def GET_RESPONSE(self):
		return

	def ENVELOPPE(self):
		return

	def SEARCH_RECORD(self):
		return

	def DISABLE_CHV(self):
		return

	def UNBLOCK_CHV(self):
		return
