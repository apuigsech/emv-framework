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
	},
	{
		'name':'GET_RESPONSE',
		'code':0xc0
	}
)

class APDU_Command:
	def __init__(self, cla=0x00, ins=0x00, p1=0x00, p2=0x00, lc=None, data=None, le=None):
		self.cla = cla
		self.ins = ins
		self.p1 = p1
		self.p2 = p2
		if data != None and lc == None:
			lc = len(data)
		self.lc = lc
		self.data = data
		self.le = le

	def raw(self):
		apdu_cmd_raw = [self.cla, self.ins, self.p1, self.p2]
		if self.data != None:
			apdu_cmd_raw += [self.lc] + self.data
		if self.le != None:
			apdu_cmd_raw += [self.le]
		return apdu_cmd_raw

	def str(self):
		apdu_cmd_str = '{0:02x} {1:02x} {2:02x} {3:02x}'.format(self.cla, self.ins, self.p1, self.p2)
		if self.data != None:
			apdu_cmd_str += ' {0:02x}'.format(self.lc)
			for d in self.data:
				apdu_cmd_str += ' {0:02x}'.format(d)
		if self.le != None:
			apdu_cmd_str += ' {0:02x}'.format(self.le)
		return apdu_cmd_str


class APDU_Response:
	def __init__(self, sw1=0x00, sw2=0x00, data=None):
		self.sw1 = sw1
		self.sw2 = sw2
		self.data = data

	def raw(self):
		apdu_res_raw = []
		if self.data != None:
			apdu_res_raw += self.data
		apdu_res_raw += [self.sw1, self.sw2]
		return apdu_res_raw

	def str(self):
		apdu_res_str = ''
		if self.data != None:
			for d in self.data:
				apdu_res_str += '{0:02x} '.format(d)
		apdu_res_str += '{0:02x} {1:02x}'.format(self.sw1, self.sw2)
		return apdu_res_str



class ISO7816:
	def __init__(self):
		cardtype = AnyCardType()
		cardrequest = CardRequest(timeout=10, cardType=cardtype)
		self.card = cardrequest.waitforcard()
		self.card.connection.connect()
		self.ins_db = []
		self.ins_db_update(INS_DB)
		self.log = []
	
		self.auto_get_response = True

	def ins_db_update(self, new): 
		self.ins_db += new

	def ins_db_resolv(self, name=None, code=None):
		for e in self.ins_db:
			if name != None and e['name'] == name:
				return e['code']
			if code != code and e['code'] == code:
				return e['name']
		return None

	def send_command(self, cmd, p1=0, p2=0, tlvparse=False, cla=0x00, data=None, le=None):
		ins = self.ins_db_resolv(name=cmd)
		return self.send_apdu(APDU_Command(ins=ins, p1=p1, p2=p2, cla=cla, data=data, le=le))

	def send_apdu(self, apdu_cmd):
		#print '>>> ' + apdu_cmd.str()
		data,sw1,sw2 = self.send_apdu_raw(apdu_cmd.raw())
		apdu_res = APDU_Response(sw1=sw1, sw2=sw2, data=data)
		#print '<<< ' + apdu_res.str()

		if (sw1 == 0x61 and self.auto_get_response == True):
			apdu_res = self.GET_RESPONSE(sw2)
	
		return apdu_res	

	def send_apdu_raw(self, apdu):
		return self.card.connection.transmit(apdu)

	def log_add(self, log_item):
		self.log.append(log_item)

	def log_print(self):
		return

	def READ_BINARY(self, p1=0x00, p2=0x00, len=0x00):
		return self.send_command('READ_BINARY', p1=p1, p2=p2, le=len)

	def WRITE_BINARY(self, p1=0x00, p2=0x00, data=[]):
		return self.send_command('WRITE_BINARY', p1=p1, p2=p2, data=data)

	def UPDATE_BINRY(self, p1=0x00, p2=0x00, data=[]):
		return self.send_command('UPDATE_BINRY', p1=p1, p2=p2, data=data)

	def ERASE_BINARY(self, p1=0x00, p2=0x00, data=None):
		return self.send_command('ERASE_BINARY', p1=p1, p2=p2, data=data)

	def READ_RECORD(self, sfi, record=0x00):
		return self.send_command('READ_RECORD', p1=record, p2=(sfi<<3)+4)

	def WRITE_RECORD(self, sfi, data, record=0x00):
		return self.send_command('WRITE_RECORD', p1=record, p2=(sfi<<3)+4, data=data)

	def APPEND_RECORD(self, sfi):
		return self.send_command('APPEND_RECORD', p1=0x00, p2=(sfi<<3), data=data)

	def UPDATE_RECORD(self, sfi, data, record=0x00):
		return self.send_command('UPDATE_RECORD', p1=record, p2=(sfi<<3)+4, data=data)

	def GET_DATA(self, data_id):
		return self.send_command('GET_DATA', p1=data_id[0], p2=data_id[1]) 

	def PUT_DATA(self, data_id, data):
		return self.send_command('PUT_DATA', p1=data_id[0], p2=data_id[1], data=data)

	def SELECT_FILE(self, data, p1=0x00, p2=0x00):
		return self.send_command('SELECT_FILE', p1=p1, p2=p2, data=data)

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

	def GET_RESPONSE(self, le):
		return self.send_command('GET_RESPONSE', le=le)

	def ENVELOPPE(self):
		return

	def SEARCH_RECORD(self):
		return

	def DISABLE_CHV(self):
		return

	def UNBLOCK_CHV(self):
		return
