#!/usr/bin/python

#
#    Python TLV (as part of EMV Framework)
#    Copyrigh 2012 Albert Puigsech Galicia <albert@puigsech.com>
#
#    This code is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#

TAG_CLASS_UNIVERSAL = 0x0
TAG_CLASS_APLICATION = 0x1
TAG_CLASS_CONTEXT_SPECIFIC= 0x2
TAG_CLASS_PRIVATE = 0x3

TAG_TYPE_PRIMITIVE = 0x0
TAG_TYPE_CONSTRUCTED = 0x1

TAG_SIZE_BIG_1 = 0x81
TAG_SIZE_BIG_2 = 0x82

class TAG:
	def __init__(self, data=None, tags_db=None):
		self.childs = [] 
		self.root = False
		self.code = None
		self.name = None
		self.type = None
		self._class = None
		self.extended = None
		self.size = None
		self.total_size = None
		self.parse(data, tags_db)

	def parse(self, data, tags_db):
		if data == None:
			return
		
		size = len(data)
		
		i = 0
		if data[i]&0b00011111 == 0b00011111:
			self.extended = True
		else:
			self.extended = False
		self._class = (data[i]&0b11000000)>>6
		self.type = (data[i]&0b00100000)>>5		

		if self.extended:
			self.code = 256 * data[i] + data[i+1]
			i += 2
		else:
			self.code = data[i]	
			i += 1

		if data[i] == TAG_SIZE_BIG_1:
			self.size = data[i+1]
			i += 2
		elif data[i] == TAG_SIZE_BIG_2:
			self.size = 256 * data[i+1] + data[i+2]
			i +=3
		else:
			self.size = data[i]
			i += 1

		self.data = data[i:i+self.size]
		i += self.size

		if self.type == TAG_TYPE_CONSTRUCTED:
			j = 0
			while j < self.size:
				tag = TAG(self.data[j:], tags_db)
				self.childs.append(tag)
				j += tag.total_size

		self.total_size = i

		if tags_db != None and tags_db.has_key(self.code):
			self.name = tags_db[self.code]['name']


	def list_childs(self, code=None):
		if code == None:
			return self.childs
		ret = []
		for c in self.childs:
			if c.code == code:
				ret.append(c)
		return ret

	def show(self, deep=0):
		if self.root:
			self.childs[0].show(deep)
		else:
			deep_str = deep*'   '
			print '%s%.2x [%.2x] - %s' % (deep_str, self.code, self.size, self.name)
			if self.type == TAG_TYPE_PRIMITIVE:
				print '%s  ' % (deep_str),
				for i in self.data:
					print '%.2x' % (i),
				print
			deep += 1
			for tag in self.childs:
				tag.show(deep)

class TLV(TAG):
	def parse(self, data, tags_db=None):
		size = len(data)
		self.root = True
		self.type = TAG_TYPE_CONSTRUCTED
		i = 0
		while i < size:
			tag = TAG(data[i:], tags_db)
			self.childs.append(tag)
			i += tag.total_size
