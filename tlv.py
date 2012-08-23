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

def tag_tags(data, size, tags_db):
	i = 0
	items = []

	while (i < size):
		tag_1 = data[i]
		tag_2 = data[i+1] + 256 * data[i]

		if tags_db.has_key(tag_2):
			i += 2
			tag = tag_2
		elif tags_db.has_key(tag_1):
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

		if (tags_db.has_key(tag)):	   
			tag_name = tags_db[tag][0]	
			tag_func = tags_db[tag][1]
		else:
			tag_name = 'Unknown tag'
			tag_func = tag_binary


		print '0x%x [0x%.2x] %s' % (tag, tag_size, tag_name)
		items.append({
			'name':tag_name,
			'size':tag_size,
			'data':tag_data,
			'content':tag_func(tag_data, tag_size, tags_db)
		})

		i += tag_size

	return items
	
	
def tag_binary(data, size, tags_db):
	i = 0

	if (len(data) < size):
		print "PARSE ERROR"
		size = len(data)

	while (i < size):
		print '%.2x' % (data[i]),
		i += 1
	print


# TODO
def tag_numeric(data, size, tags_db):
	i = 0


def tag_string(data, size, tags_db):
	i = 0
	while (i < size):
		print '%c' % (data[i]),
		i += 1
	print

def tag_object(data, size, tags_db):
	i = 0
	while(i < size):
		tag_1 = data[i]
		tag_2 = data[i+1] + 256 * data[i]

		if tags_db.has_key(tag_1):
			i += 1
			tag = tag_1
		elif tags_db.has_key(tag_2):
			i += 2
			tag = tag_2
		else:
			i += 1
			tag = tag_1

		tag_size = data[i]
		i += 1

                if (tags_db.has_key(tag)):
                        tag_name = tags_db[tag][0]
                        tag_func = tags_db[tag][1]
                else:
                        tag_name = 'Unknown tag'
                        tag_func = tag_binary

                print ' * 0x%x [0x%.2x] %s' % (tag, tag_size, tag_name)

TAG_TAGS = tag_tags
TAG_BINARY = tag_binary
TAG_NUMERIC = tag_numeric
TAG_STRING = tag_string
TAG_OBJECT = tag_object

# TODO: Create a tree with the information but not print it.

class TLV:
	def __init__(self, tags_db={}):
		self.tags_db = tags_db
		self.data = []

	def parse(self, data):
		self.data = tag_tags(data, len(data), self.tags_db)
		return self.data

	def show(self, data=None, deep=0):
		if data == None:
			data = self.data
		for i in data:
			print i
