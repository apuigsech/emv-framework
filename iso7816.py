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

class ISO7816:
	def __init__(self):
		cardtype = AnyCardType()
		cardrequest = CardRequest(timeout=10, cardType=cardtype)
		self.card = cardrequest.waitforcard()
		self.card.connection.connect()
		self.ins_db = []
		self.ins_db_update(INS_DB)
		self.log = []

	def ins_db_update(self, new): 
		self.ins_db += new

	def ins_db_resolv(self, name=None, code=None):
		for e in self.ins_db:
			if name != None and e['name'] == name:
				return e['code']
			if code != code and e['code'] == code:
				return e['name']
			
		return None

	def send_command(self, cmd, p1, p2, tlvparse=False, cla=0x00, data=None, le=None):
		ins = self.ins_db_resolv(name=cmd)
		res,sw1,sw2 = self.send_apdu(ins=ins, p1=p1, p2=p2, cla=cla, data=data, le=le)
		# TODO: Check sw1 and sw2
		if tlvparse == True:
			tlv = TLV(res)
			return res,sw1,sw2,tlv
		else:
			return res,sw1,sw2,None

	def send_apdu(self, ins, p1, p2, cla=0x00, data=None, le=None):
		apdu = [cla, ins, p1, p2]
		if data != None:
			apdu += [len(data)] + data
		if le != None:
			apdu += le
		return self.send_apdu_raw(apdu)

	def send_apdu_raw(self, apdu):
		res,sw1,sw2 = self.card.connection.transmit(apdu)
		log_item = {
			'request':apdu,
			'response':res,
			'sw1':sw1,
			'sw2':sw2
		}
		self.log_add(log_item)
		return res,sw1,sw2

	def log_add(self, log_item):
		self.log.append(log_item)

	def log_print(self):
		for l in self.log:
			print '>>>> ' + l['request']
			print '<<<< ' + l['response'] + ' SW1: ' + l['sw1'] + ' SW2: ' + l['sw2']	
	
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
		self.send_command('PUT_DATA', p1=data_id[0], p2=data_id[1], data=data)

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
