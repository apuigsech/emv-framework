#!/usr/bin/python

#
#    Python AID (as part of EMV Framework)
#    Copyrigh 2012 Albert Puigsech Galicia <albert@puigsech.com>
#
#    This code is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#


AID_DB = (
	{
		'name':'visa',
		'print_name':'VISA',
		'code':[0xa0,0x00,0x00,0x00,0x03],
		'child':(
			{
				'name':'debit_credit',
				'print_name':'Debit/Credit',
				'code':[0x10,0x10]
			},
			{
				'name':'electron',
				'print_name':'Electron',
				'code':[0x20,0x10]
			},
			{
				'name':'v_pay',
				'print_name':'V PAY',
				'code':[0x20,0x20]
			},
			{
				'name':'plus',
				'print_name':'Plus',
				'code':[0x80,0x10]
			}
		)
	},
	{
		'name':'mastercard',
		'print_name':'MasterCard',
		'code':[0xa0,0x00,0x00,0x00,0x04],
		'child':(
			{
				'name':'debit_credit',
				'print_name':'Debit/Credit',
				'code':[0x10,0x10]
			},
			{
				'name':'mastercard',
				'print_name':'MasterCard',
				'code':[0x99,0x99]
			},
			{
				'name':'maestro',
				'print_name':'Maestro',
				'code':[0x30,0x60]
			},
			{
				'name':'cirrus',
				'print_name':'Cirrus',
				'code':[0x60,0x00]
			}
		)
	},
	{
		'name':'uk_domestic',
		'print_name':'UK Domestic',
		'code':[0xa0,0x00,0x00,0x00,0x05],
		'child':(
			{
				'name':'maestro',
				'print_name':'Maestro',
				'code':[0x00,0x01]
			},
			{
				'name':'solo',
				'print_name':'Solo',
				'code':[0x00,0x02]
			}
		)
	},
	{
		'name':'american_express',
		'print_name':'American Express',
		'code':[0xa0,0x00,0x00,0x00,0x25],
		'child':(
			{
				'name':'american_express',
				'print_name':'American Express',
				'code':[0x01]
			}
		)
	},
	{
		'name':'rupay',
		'print_name':'RuPay',
		'code':[0xa0,0x00,0x00,0x05,0x24],
		'child':(
			{
				'name':'rupay',
				'print_name':'RuPay',
				'code':[0x10,0x10]
			}
		)
	},
	{
		'name':'discover',
		'print_name':'Discover',
		'code':[0xa0,0x00,0x00,0x01,0x52],
		'child':(
			{
				'name':'discover',
				'print_name':'Discover',
				'code':[0x30,0x10]
			}
		)
	},
	{
		'name':'interact',
		'print_name':'Interact',
		'code':[0xa0,0x00,0x00,0x02,0x77],
		'child':(
			{
				'name':'debit',
				'print_name':'Debit',
				'code':[0x10,0x10]
			}
		)
	},
	{
		'name':'jbc',
		'print_name':'Japan Credit Bureau',
		'code':[0xa0,0x00,0x00,0x00,0x65],
		'child':(
			{
				'name':'jbc',
				'print_name':'Japan Credit Bureau',
				'code':[0x10,0x10]
			}
		)
	},
	{
		'name':'link',
		'print_name':'LINK',
		'code':[0xa0,0x00,0x00,0x00,0x29],
		'child':(
			{
				'name':'atm',
				'print_name':'ATM',
				'code':[0x10,0x10]
			}
		)
	},
	{
		'name':'dankort',
		'print_name':'DanKort',
		'code':[0xa0,0x00,0x00,0x01,0x21],
		'child':(
			{
				'name':'debit',
				'print_name':'Debit',
				'code':[0x10,0x10]
			}
		)

	},
	{
		'name':'cogeban',
		'print_name':'CoGeBan',
		'code':[0xa0,0x00,0x00,0x01,0x41],
		'child':(
			{
				'name':'pagobancomat',
				'print_name':'PagoBANCOMAT',
				'code':[0x00,0x01]
			}
		)
	},
	{
		'name':'banrisul',
		'print_name':'Banrisul',
		'code':[0xa0,0x00,0x00,0x01,0x54],
		'child':(
			{
				'name':'banricompras_debito',
				'print_name':'Banricompras Debito',
				'code':[0x44,0x42]
			}
		)
	},
	{
		'name':'zka',
		'print_name':'ZKA',
		'code':[0xa0,0x00,0x00,0x03,0x59],
		'child':(
			{
				'name':'girocard',
				'print_name':'Girocard',
				'code':[0x10,0x10,0x02,0x80,0x01]
			}
		)
	},
	{
		'name':'cb',
		'print_name':'CB',
		'code':[0xa0,0x00,0x00,0x00,0x42],
		'child':(
			{
				'name':'cb',
				'print_name':'CB',
				'code':[0x10,0x10]
			}
		)
	},
	{
		'name':'span',
		'print_name':'SPAN',
		'code':[0xa0,0x00,0x00,0x02,0x28],
		'child':(
			{
				'name':'span1',
				'print_name':'SPAN1',
				'code':[0x10,0x10]
			},
			{
				'name':'span2',
				'print_name':'SPAN2',
				'code':[0x20,0x10]
			}
		)
	}
)

class AID:
	def __init__(self,name=None,code=None):
		self.name = None
		self.print_name = None
		self.code = None
		if (name != None):
			self.from_name(name)
		if (code != None):
			self.from_code(code)

	def from_name(self,n):
		name = ''
		print_name = ''
		code = []
		current_db = AID_DB
		for sn in n.split('.'):
			match = False
			for e in current_db:
				if e['name'] == sn:
					match = True
					code += e['code']
					name += e['name'] + '.' 
					print_name += e['print_name'] + ' '
					if e.has_key('child'):
						current_db = e['child']
					break
			if match == False:
				return
		self.name = name[:-1]
		self.print_name = print_name[:-1]
		self.code = code
		
	def from_code(self,c):
		name = ''
		print_name = ''
		code = c
		current_db = AID_DB
		i = 0
		while(i < len(c)):
			for e in current_db:
				match = False
				if e['code'] == c[i:i+len(e['code'])]:		
					match = True
					i += len(e['code'])
					name += e['name'] + '.'
					print_name += e['print_name'] + ' '
					if e.has_key('child'):
						current_db = e['child']
					break
			if match == False:
				while(i < len(c)):
					name += '%x' % (c[i]) + '.'
					print_name += '%x' % (c[i]) + ' ' 
					i += 1
		self.name = name[:-1]
		self.print_name = print_name[:-1]
		self.code = code
