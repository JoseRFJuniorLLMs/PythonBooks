# dictionary queries
"""dictlist.py

Assume we have a list of dictionaries.  This extracts tabular data
from them, and provides common operations useful on such a list
"""

import doubletalk.datastruct

def GetKeys(dictlist):
	"lists all the keys in all the dictionaries"
	s = doubletalk.datastruct.Set()
	for dict in dictlist:
		for key in dict.keys():
			s.add(key)
	return s.elements()

def Tabulate(dictlist, keylist=None):
	"returns a tabular data set for given keys"
	if keylist == None:
		keylist = GetKeys(dictlist)
	result = []
	for dict in dictlist:
		row = []
		for key in keylist:
			try:
				row.append(dict[key])
			except KeyError:
				row.append(None)
		result.append(tuple(row))
	return result
		
	
def SelectHavingKey(dictlist, key):
	"returns all dicts which have a certain key"
	result = []
	for dict in dictlist:
		if dict.has_key(key):
			result.append(dict)
	return result

def SelectHavingKeyAndValue(dictlist, key, value):
	"returns all dicts which have a certain key"
	result = []
	for dict in dictlist:
		try:
			if dict[key] == value:
				result.append(dict)
		except:	
			pass
	return result


def MakeDictList(count=100):
	"Makes some sample data"
	from random import choice, random

	Products = ['Widgets','Sprockets','Gaskets','Thingies','Wotsits']
	Stores = ['Putney','Clapham','Wimbledon','Richmond','Fulham']
	Months = [9801,9802,9803,9804,9805]
	result = []
	
	for i in range(count):
		dict = {}
		dict['Amount'] = int(1000 * random())
		dict['Month'] = choice(Months)
		dict['NominalAccount'] = 'Sales'
		dict['Product'] = choice(Products)
		dict['Store'] = choice(Stores)
		result.append(dict)
	
	return result
