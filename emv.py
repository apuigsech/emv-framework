#!/usr/bin/python

#
#    Python EMV Framework
#    Copyrigh 2012 Albert Puigsech Galicia <albert@puigsech.com>
#
#    This code is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#

from lxml import etree

from tlv import *
from aid import *
from iso7816 import ISO7816

# TODO: Solve conflicts with ISO7816 in DB (EXTERNAL_AUTHENTICATE, GET_CHALLENGE)

INS_DB = (
	{
		'name':'APPLICATION_BLOCK',
		'code':0x1e
	},
	{
		'name':'APPLICATION_UNBLOCK',
		'code':0x18
	},
	{
		'name':'CARD_BLOCK',
		'code':0x16
	},
	{
		'name':'EXTERNAL_AUTHENTICATE',
		'code':0x82
	},
	{
		'name':'GENERATE_APPLICATION_CRYPTOGRAM',
		'code':0xae
	},
	{
		'name':'GET_CHALLENGE',
		'code':0x84
	},
	{
		'name':'GET_PROCESSING_OPTIONS',
		'code':0xa8
	},
	{
		'name':'PIN_CHANGEUNBLOCK',
		'code':0x24
	}
)

class EMV(ISO7816):
	def __init__(self):
		ISO7816.__init__(self)
		ISO7816.ins_db_update(self, INS_DB)
		return

	def SELECT_AID(self, aid):
		return self.SELECT_FILE(data=aid, p1=0x04, p2=0x00)
	
	def APPLICATION_BLOCK(self, mac, cla=0x00, p1=0x00, p2=0x00):
		ins = self.ins_db_resolv('APPLICATION_BLOCK')
		self.send_apdu(ins=ins, cla=cla, p1=p1, p2=p2, data=mac)

	def APPLICATION_UNBLOCK(self, mac, cla=0x00, p1=0x00, p2=0x00):
                ins = self.ins_db_resolv('APPLICATION_UNBLOCK')
                self.send_apdu(ins=ins, cla=cla, p1=p1, p2=p2, data=mac)

	def CARD_BLOCK(self, mac, cla=0x00, p1=0x00, p2=0x00):
                ins = self.ins_db_resolv('CARD_BLOCK')
                self.send_apdu(ins=ins, cla=cla, p1=p1, p2=p2, data=mac)

	def EXTERNAL_AUTHENTICATE(self):
                return

	def GENERATE_APPLICATION_CRYPTOGRAM(self):
		return

	def GET_CHALLENGE(self):
		return

	def GET_PROCESSING_OPTIONS(self, pdol_data, p1=0x00, p2=0x00):
		data = [0x83, len(pdol_data)] + pdol_data
		return self.send_command('GET_PROCESSING_OPTIONS', cla=0x80, p1=p1, p2=p2, data=data)
		return apdu_res

	def PIN_CHANGEUNLOCK(self):
                return

class EMV_TLV(TLV):
	def __init__(self, data=None, content=True):
		tags_db = {}

		tree = etree.parse('data/emv_tags.xml')
		for tag in tree.findall('tag'):
			if tag.attrib.has_key('name'):
				name = tag.attrib['name']
			else:
				name = ''
			if tag.attrib.has_key('parser'):
				parser = 'emv.{0:s}'.format(tag.attrib['parser'])
			else:
				parser = None

			tags_db[tag.attrib['code']] = {
				'name':name,
				'parser':parser
			}

		TLV.__init__(self, data, tags_db, content)

def tag_string(tag, show=None):
	tag.human_data = ''.join(map(chr,tag.data))
			

def tag_dol(tag, show=None):
	tlv = EMV_TLV(tag.data, content=False)
	tag.parsed_data = []
	for c in tlv.childs:
		tag.parsed_data.append(c)
		tag.childs.append(c)

def tag_aid(tag, show=None):
	tag.human_data = AID(code=tag.data).name
