#/usr/bin/python

#
#    Python EMV Framework
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

import sys

# TODO: Add more AIDs
AID = {
	'VISA':[0xa0,0x00,0x00,0x00,0x03],
	'VISA Debit/Credit':[0xa0,0x00,0x00,0x00,0x03,0x10,0x10]
}

# TODO: Complete response codes, and maybe a 'helper' to manage responses.
# http://www.scard.org/software/info.html

RES = {
	0x69:{
		0x81:'Command incompatible with file structure',
		0x82:'Security status not satisfied',
		0x85:'',
		0x86:'Command not allowed (no current EF)'
	},
	0x6a:{
		0x81:'Function not supported',
		0x82:'File not found',
		0x83:'Record not found'
	},
	0x6d:{
		0x00:'Intruction code not suported or invalid'
	},
	0x90:{
		0x00:'OK'
	}
}

class EMV_Framework:
	def init_card(self):
		cardtype = AnyCardType()
		cardrequest = CardRequest(timeout=10, cardType=cardtype)
		self.card = cardrequest.waitforcard()
        	self.card.connection.connect()
	
	def send_apdu(self, cli, ins, p1, p2, data=None, le=None):
		apdu = [cli] + [ins] + [p1] + [p2]
		if data != None:
			apdu += [len(data)] + data
		if le != None:
			apdu += [le]

		return self.send_apdu_raw(apdu)

	def send_apdu_raw(self, apdu):
		res, sw1, sw2 = self.card.connection.transmit(apdu)
		return res,sw1,sw2
	
	# TODO
	def application_block(self):
		return self.send_apdu(0x84, 0x1e, 0x00,0x0)

	# TODO
	def application_unlock(self):
		return self.send_apdu(0x84, 0x18, 0x00, 0x00)

	def compute_cryptogram(self, un):
		return self.send_apdu(0X80, 0x2a, 0x8e, 0x80, un, 0x00)

	def get_processing_options(self, pdol_data):
		data = [0x83, len(pdol_data)] + pdol_data
		return self.send_apdu(0x80, 0xa8, 0x00, 0x00, data, 0x00)

	def read_record(self, record, sfi):
		return self.send_apdu(0x00, 0xb2, record, (sfi << 3)+4, le=0x00)

	def read_data(self, data):
		return self.send_apdu(0x80, 0xca, data[0], data[1], le=0x00)

	# TODO
	def get_challenge(self):
		return

	def select_aid(self, aid):
		return self.send_apdu(0x00, 0xa4, 0x04, 0x00, aid, 0x00)
