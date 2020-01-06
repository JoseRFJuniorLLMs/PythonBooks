# OLAP stuff
# quick example to get my head in gear

"""  OLAP.py

This is a rough attempt at a 'hypercube' for holding data.  Given a list
of tuple of data like
[	# amt    month        product   store
	(100.00, 199703, Widgets, Clapham),
	(17.00, 199704, Sprockets, Tadley),
	...
]

It builds a multidimensional array with the amounts in the middle and the 
category names in the outermost cells.  

To make life easy, we assume a class we build ONCE and do not modify after.
Each dimension is a simple list of categories.  
"""

import doubletalk.datastruct
import doubletalk.dictlist

class Dimension:
	"needs work!  A list of categories"
	def __init__(self):
		self.name = '<unnamed>'
		self.values = []

	def IndexOf(self, keyword):
		try:
			return self.values.index(keyword)
		except ValueError:
			return -1
		

class HyperCube:
	def __init__(self, rows):
		self.rows = rows   # keep a them for drill-down - should really copy
		self.dimensions = []
		self.dimcount = 0
		self.data = doubletalk.datastruct.NumDict()
		self.ProcessRows(rows)


	def ProcessRows(self, rows):
		# first count dimensions
		self.dimcount = len(rows[0]) - 1
		
		# now categorize them - get a list of buckets for each
		for i in range(self.dimcount):
			dim = Dimension()
			dim.name = 'Dimension %d' % (i+1)
			dim.values = Categorize(rows, i+1)
			self.dimensions.append(dim)
			
		# now make a sparse matrix with the values
		for row in self.rows:
			key = tuple(row[1:])
			value = row[0]
			self.data.inc(key, value)
	
	def Value(self, keylist):
		return self.data[tuple(keylist)]	
	
	def DrillDown(self, keylist):
		"gets a list of the items representing a point in the cube."
		# Searches entire dataset - could be improved with sorting
		
		found = []
		#make sure we have a tuple, to compare with rows
		keylist = tuple(keylist) 
		for row in self.rows:
			if row[1:] == keylist:
				found.append(row)
		return found
	
	
	def PrintInfo(self):
		"Basic report on available dimensions"
		print "Fact Count: ", len(self.rows)
		print "Dimension Count: ",self.dimcount
		for i in range(self.dimcount):
			dim = self.dimensions[i]
			
			#first 40 character of dimension values
			text = repr(dim.values)
			if len(text) > 60:
				text = text[0:60]
			
			print '%d  %-15s   %-40s' % (i+1, dim.name, text)
	
def Categorize(aDataSet, DimNo):
	"Returns the set of unique values of a given column, sorted"
	ValSet = {}
	for row in aDataSet:
		ValSet[row[DimNo]] = 1
	ValList = ValSet.keys()
	ValList.sort()
	return ValList


def MakeData(count=100):
	# makes tuples
	from random import choice, random

	Products = ['Widgets','Sprockets','Gaskets','Thingies','Wotsits']
	Stores = ['Putney','Clapham','Wimbledon','Richmond','Fulham']
	Months = [9801,9802,9803,9804,9805]
	
	result = []
	
	for i in range(count):
		amount = int(1000 * random())
		prod = choice(Products)
		store = choice(Stores)
		months = choice(Months)
		result.append((amount, prod, store, months))
	
	return result
		




def test(count=10000):
	"give it a workout"
	import time
	
	t0 = time.time()
	print "Building %d random dictionaries of data..." % (count)
	dictlist = doubletalk.dictlist.MakeDictList(count)
	
	print "extracting all keys"
	keys = doubletalk.dictlist.GetKeys(dictlist)
	
	#hopefully 'Amount' is first in alpha order!
	
	print "tabulating data..."
	table = doubletalk.dictlist.Tabulate(dictlist, keys)
	
	print 'building a hypercube...'
	cube = HyperCube(table)
	cube.PrintInfo()
	
	print
	sought = (9804,'Sales','Gaskets','Putney')
	value = cube.Value(sought)
	print 'Sales of Putney Gaskets in April: %f' % (value)
	print
	
	print 'drilling down to raw data...'
	rows = cube.DrillDown(sought)
	print len(rows), 'rows found, displaying first few'	
	if len(rows) > 5:
		rows = rows[0:5]
	for row in rows:
		print '\t',row

	
	t1 = time.time()
	print 'Time: %f seconds' % (t1 - t0)


if __name__ == '__main__':
	test()