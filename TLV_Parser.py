#!/usr/bin/python

#
#    Python TLV Parser (as part of EMV Framework)
#    Copyrigh 2012 Albert Puigsech Galicia <albert@puigsech.com>
#
#    This code is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#

def tag_tags(data, size):
	i = 0

	while (i < size):
		tag_1 = data[i]
		tag_2 = data[i+1] + 256 * data[i]

		if TLV_TAGS.has_key(tag_2):
			i += 2
			tag = tag_2
		elif TLV_TAGS.has_key(tag_1):
			i += 1
			tag = tag_1
		else:
			i += 1
			tag = tag_1
	
		tag_size = data[i]
		if (tag_size == 0x81):
			i += 1
			tag_size = data[i]
		i += 1
		tag_data = data[i:i+tag_size]

		if (TLV_TAGS.has_key(tag)):	   
			tag_name = TLV_TAGS[tag][0]	
			tag_func = TLV_TAGS[tag][1]
		else:
			tag_name = 'Unknown tag'
			tag_func = tag_binary

		print '0x%x [0x%.2x] %s' % (tag, tag_size, tag_name)
		tag_func(tag_data, tag_size)
		i += tag_size
	
	
def tag_binary(data, size):
	i = 0

	if (len(data) < size):
		print "PARSE ERROR"
		size = len(data)

	while (i < size):
		print '%.2x' % (data[i]),
		i += 1
	print


# TODO
def tag_numeric(data, size):
	i = 0


def tag_string(data, size):
	i = 0
	while (i < size):
		print '%c' % (data[i]),
		i += 1
	print

def tag_object(data, size):
	i = 0
	while(i < size):
		tag_1 = data[i]
		tag_2 = data[i+1] + 256 * data[i]

		if TLV_TAGS.has_key(tag_1):
			i += 1
			tag = tag_1
		elif TLV_TAGS.has_key(tag_2):
			i += 2
			tag = tag_2
		else:
			i += 1
			tag = tag_1

		tag_size = data[i]
		i += 1

                if (TLV_TAGS.has_key(tag)):
                        tag_name = TLV_TAGS[tag][0]
                        tag_func = TLV_TAGS[tag][1]
                else:
                        tag_name = 'Unknown tag'
                        tag_func = tag_binary

                print ' * 0x%x [0x%.2x] %s' % (tag, tag_size, tag_name)


CVM = {
	0x00:'Fail CVM processing',
	0x01:'Plaintext PIN verified offline',
	0x02:'Enciphered PIN verified online',
	0x03:'Plaintext PIN verified offline and signature (paper)',
	0x04:'Enciphered PIN verified offline',
	0x05:'Enciphered PIN verified offline and signature (paper)',
	0x1e:'Signature (paper)',
	0x1f:'No CVM required',   
	0x3f:'Not available'
}

def tag_cvm_list(data, size):
	if size < 10:
		print "PARSE ERROR"
		return
	
	amount_1 = data[0:4]
	amount_2 = data[4:8]

	print '* Amount X: ' + str(amount_1)
	print '* Amount Y: ' + str(amount_2)

	i = 8
	while (i < size):
		cvm = data[i]
		rule = data[i+1]	
		i += 2
	
		if cvm|0b01000000:
			fail_action = 'fail'
		else:
			fail_action = 'next'
		
		cvm = cvm&0b00111111

		print '* CVM: ' + CVM[cvm] + " - " + str(rule)


# TODO: Add function to manage some specific tags.

TAG_TAGS = tag_tags
TAG_BINARY = tag_binary
TAG_NUMERIC = tag_numeric
TAG_STRING = tag_string
TAG_OBJECT = tag_object
TAG_CVM_LIST = tag_cvm_list

TLV_TAGS = {
	0x42:('Issuer Identification Number (IIN)',TAG_TAGS),
	0x4f:('Application Identifier (AID)',TAG_TAGS),
	0x50:('Application Label',TAG_STRING),
	0x57:('Track 2 Equivalent Data',TAG_BINARY),
	0x5a:('Application Primary Account Number (PAN)',TAG_BINARY),
	0x61:('Application Template',TAG_TAGS),
	0x6f:('File Control Information (FCI) Template',TAG_TAGS),
	0x70:('EMV Proprietary Template',TAG_TAGS),
	0x71:('Issuer Script Template 1',TAG_TAGS),
	0x72:('Issuer Script Template 2',TAG_TAGS),
	0x73:('Directory Discretionary Template',TAG_TAGS),
	0x77:('Response Message Template Format 2',TAG_TAGS),
	0x80:('Response Message Template Format 1',TAG_TAGS),
	0x81:('Amount, Authorised (Binary)',TAG_TAGS),
	0x82:('Application Interchange Profile',TAG_BINARY),
	0x83:('Command Template',TAG_BINARY),
	0x84:('Dedicated File (DF) Name',TAG_BINARY),
	0x86:('Issuer Script Command',TAG_TAGS),
	0x87:('Application Priority Indicator',TAG_BINARY),
	0x88:('Short File Identifier (SFI)',TAG_TAGS),
	0x89:('Authorisation Code',TAG_TAGS),
	0x8a:('Authorisation Response Code',TAG_TAGS),
	0x8c:('Card Risk Management Data Object List 1 (CDOL1)',TAG_OBJECT),
	0x8d:('Card Risk Management Data Object List 2 (CDOL2)',TAG_OBJECT),
	0x8e:('Cardholder Verification Method (CVM) List',TAG_CVM_LIST),
	0x8f:('Certification Authority Public Key Index',TAG_BINARY),
	0x90:('Issuer Public Key Certificate',TAG_BINARY),
	0x91:('Issuer Authentication Data',TAG_TAGS),
	0x92:('Issuer Public Key Remainder',TAG_BINARY),
	0x93:('Signed Static Application Data',TAG_TAGS),
	0x94:('Application File Locator (AFL)',TAG_TAGS),
	0x95:('Terminal Verification Results',TAG_TAGS),
	0x97:('Transaction Certificate Data Object List (TDOL)',TAG_TAGS),
	0x98:('Transaction Certificate (TC) Hash Value',TAG_TAGS),
	0x99:('Transaction Personal Identification Number (PIN) Data',TAG_TAGS),
	0x9a:('Transaction Date',TAG_TAGS),
	0x9b:('Transaction Status Information',TAG_TAGS),
	0x9c:('Transaction Type',TAG_TAGS),
	0x9d:('Directory Definition File (DDF) Name',TAG_TAGS),
	0xa5:('File Control Information (FCI) Proprietary Template',TAG_TAGS),
	0x5f20:('Cardholder Name',TAG_STRING),
	0x5f24:('Application Expiration Date',TAG_BINARY),
	0x5f25:('Application Effective Date',TAG_TAGS),
	0x5f28:('Issuer Country Code',TAG_BINARY),
	0x5f2a:('Transaction Currency Code',TAG_TAGS),
	0x5f2d:('Language Preference',TAG_TAGS),
	0x5f30:('Service Code',TAG_BINARY),
	0x5f34:('Application Primary Account Number (PAN)',TAG_BINARY),
	0x5f36:('Transaction Currency Exponent',TAG_TAGS),
	0x5f50:('Issuer URL',TAG_TAGS),
	0x5f53:('International Bank Account Number (IBAN)',TAG_TAGS),
	0x5f54:('Bank Identifier Code (BIC)',TAG_TAGS),
	0x5f55:('Issuer Country Code (alpha2 format)',TAG_STRING),
	0x5f56:('Issuer Country Code (alpha3 format)',TAG_TAGS),
	0x9f01:('Acquirer Identifier',TAG_TAGS),
	0x9f02:('Amount, Authorised (Numeric)',TAG_TAGS),
	0x9f03:('Amount, Other (Numeric)',TAG_TAGS),
	0x9f04:('Amount, Other (Binary)',TAG_TAGS),
	0x9f05:('Application Discretionary Data',TAG_TAGS),
	0x9f06:('Application Identifier (AID) - terminal',TAG_TAGS),
	0x9f07:('Application Usage Control',TAG_BINARY),
	0x9f08:('Application Version Number',TAG_BINARY),
	0x9f09:('Application Version Number',TAG_TAGS),
	0x9f0b:('Cardholder Name Extended',TAG_TAGS),
	0x9f0d:('Issuer Action Code - Default',TAG_BINARY),
	0x9f0e:('Issuer Action Code - Denial',TAG_BINARY),
	0x9f0f:('Issuer Action Code - Online',TAG_BINARY),
	0x9f10:('Issuer Application Data',TAG_BINARY),
	0x9f11:('Issuer Code Table Index',TAG_TAGS),
	0x9f12:('Application Preferred Name',TAG_TAGS),
	0x9f13:('Last Online Application Transaction Counter (ATC) Register',TAG_BINARY),
	0x9f14:('Lower Consecutive Offline Limit',TAG_TAGS),
	0x9f15:('Merchant Category Code',TAG_TAGS),
	0x9f16:('Merchant Identifier',TAG_TAGS),
	0x9f17:('Personal Identification Number (PIN) Try Counter',TAG_BINARY),
	0x9f18:('Issuer Script Identifier',TAG_TAGS),
	0x9f1a:('Terminal Country Code',TAG_TAGS),
	0x9f1b:('Terminal Floor Limit',TAG_TAGS),
	0x9f1c:('Terminal Identification',TAG_TAGS),
	0x9f1d:('Terminal Risk Management Data',TAG_TAGS),
	0x9f1e:('Interface Device (IFD) Serial Number',TAG_TAGS),
	0x9f1f:('Track 1 Discretionary Data',TAG_BINARY),
	0x9f20:('Track 2 Discretionary Data',TAG_TAGS),
	0x9f21:('Transaction Time',TAG_TAGS),
	0x9f22:('Certification Authority Public Key Index',TAG_TAGS),
	0x9f23:('Upper Consecutive Offline Limit',TAG_TAGS),
	0x9f26:('Application Cryptogram',TAG_BINARY),
	0x9f27:('Cryptogram Information Data',TAG_TAGS),
	0x9f2d:('Integrated Circuit Card (ICC) PIN Encipherment Public Key Certificate',TAG_TAGS),
	0x9f2e:('Integrated Circuit Card (ICC) PIN Encipherment Public Key Exponent',TAG_TAGS),
	0x9f2f:('Integrated Circuit Card (ICC) PIN Encipherment Public Key Remainder',TAG_TAGS),
	0x9f32:('Issuer Public Key Exponent',TAG_BINARY),
	0x9f33:('Terminal Capabilities',TAG_TAGS),
	0x9f34:('Cardholder Verification Method (CVM) Results',TAG_TAGS),
	0x9f35:('Terminal Type',TAG_TAGS),
	0x9f36:('Application Transaction Counter (ATC)',TAG_BINARY),
	0x9f37:('Unpredictable Number',TAG_TAGS),
	0x9f38:('Processing Options Data Object List (PDOL)',TAG_OBJECT),
	0x9f39:('Point-of-Service (POS) Entry Mode',TAG_TAGS),
	0x9f3a:('Amount, Reference Currency',TAG_TAGS),
	0x9f3b:('Application Reference Currency',TAG_TAGS),
	0x9f3c:('Transaction Reference Currency Code',TAG_TAGS),
	0x9f3d:('Transaction Reference Currency Exponent',TAG_TAGS),
	0x9f40:('Additional Terminal Capabilities',TAG_TAGS),
	0x9f41:('Transaction Sequence Counter',TAG_TAGS),
	0x9f42:('Application Currency Code',TAG_TAGS),
	0x9f43:('Application Reference Currency Exponent',TAG_TAGS),
	0x9f44:('Application Currency Exponent',TAG_TAGS),
	0x9f45:('Data Authentication Code',TAG_TAGS),
	0x9f46:('Integrated Circuit Card (ICC) Public Key Certificate',TAG_BINARY),
	0x9f47:('Integrated Circuit Card (ICC) Public Key Exponent',TAG_BINARY),
	0x9f48:('Integrated Circuit Card (ICC) Public Key Remainder',TAG_BINARY),
	0x9f49:('Dynamic Data Authentication Data Object List (DDOL)',TAG_OBJECT),
	0x9f4a:('Static Data Authentication Tag List',TAG_BINARY),
	0x9f4b:('Signed Dynamic Application Data',TAG_TAGS),
	0x9f4c:('ICC Dynamic Number',TAG_TAGS),
	0x9f4d:('Log Entry',TAG_TAGS),
	0x9f4e:('Merchant Name and Location',TAG_TAGS),
	0x9f4f:('Log Format',TAG_TAGS),
	0xbf0c:('File Control Information (FCI) Issuer Discretionary Data',TAG_TAGS),

	0xdf01:('Reference PIN',TAG_BINARY),
 	0x9f51:('Application Currency Code', TAG_BINARY),
	0x9f52:('Card Verification Results (CVR)',TAG_BINARY), 
	0x9f53:('Consecutive Transaction Limit (International)',TAG_BINARY), 
	0x9f54:('Cumulative Total Transaction Amount Limit',TAG_BINARY), 
	0x9f55:('Geographic Indicator',TAG_BINARY),
	0x9f56:('Issuer Authentication Indicator',TAG_BINARY),
 	0x9f57:('Issuer Country Code',TAG_BINARY),
 	0x9F58:('Lower Consecutive Offline Limit (Card Check)',TAG_BINARY),
	0x9f59:('Upper Consecutive Offline Limit (Card Check)',TAG_BINARY), 
	0x9f5a:('Issuer URL2',TAG_BINARY), 
	0x9f5c:('Cumulative Total Transaction Amount Upper Limit',TAG_BINARY), 
 	0x9f72:('Consecutive Transaction Limit (International - Country)',TAG_BINARY), 
	0x9f73:('Currency Conversion Factor',TAG_BINARY), 
	0x9f74:('VLP Issuer Authorization Code',TAG_BINARY), 
	0x9f75:('Cumulative Total Transaction Amount Limit - Dual Currency',TAG_BINARY), 
	0x9f76:('Secondary Application Currency Code',TAG_BINARY), 
	0x9f77:('VLP Funds Limit',TAG_BINARY), 
	0x9f78:('VLP Single Transaction Limit',TAG_BINARY), 
	0x9f79:('VLP Available Funds',TAG_BINARY), 
	0x9f7f:('Card Production Life Cycle (CPLC) History File Identifiers',TAG_BINARY), 
	0xbf0c:('FCI Issuer Discretionary Data',TAG_BINARY),

	0x9f65:('Track 2 Bit Map for CVC3',TAG_BINARY),
	0x9f66:('Track 2 Bit Map for UN and ATC',TAG_BINARY),
	0x9f68:('Mag Stripe CVM List',TAG_BINARY),
	0x9f69:('Unpredictable Number Data Object List (UDOL)',TAG_BINARY),
	0x9f6b:('Track 2 Data',TAG_BINARY),
	0x9f6c:('Mag Stripe Application Version Number (Card)',TAG_BINARY),
	0x9f6e:('Unknown Tag',TAG_BINARY),
	0x9f7d:('Unknown Tag',TAG_STRING)
}


# TODO: Create a tree with the information but not print it.

class TLV_Parser:
	def parse(self, data, size):
		tag_tags(data, size)
