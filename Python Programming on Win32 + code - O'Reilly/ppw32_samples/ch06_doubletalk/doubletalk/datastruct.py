# Copyright Andy Robinson 1998
# some generic data structures

# see the Language Reference under 3.3, Special Method Names


class Set:
	"minimal implementation to help clarity of code elsewhere"
	def __init__(self):
		self.data = {}
	def contains(self, element):
		return self.data.has_key(element)
	def add(self, element):
		self.data[element] = 1
	def elements(self):
		keys = self.data.keys()
		keys.sort()
		return keys
		
		

class NumDict:
	"""Dictionary to categorize numbers.  Usage:
	>>> import numdict
	>>> d = numdict.NumDict()
	>>> d['North'] = 100    # direct assignment
	>>> d.inc('North', 50)  # increment
	>>> d.inc('East', 130)  
	>>> d['East']
	130
	>>> d['South']
	0
	>>> d.items()
	[('East', 130), ('North', 150)]"""
	
	def __init__(self, input = None):
		self.data = {}
		if input is not None:
			for item in input:
				(category, value) = item
				self.inc(category, value)	
		

	def __getitem__(self, key):
		return self.data.get(key, 0)
		#try:
		#	return self.data[key]
		#except KeyError:
		#	return 0

	def __setitem__(self, key, value): 
		self.data[key] = value
    
	def inc(self, key, value):
		self.data[key] = self.data.get(key, 0) + value
		#try:
		#	self.data[key] = self.data[key] + value
		#except KeyError:
		#	self.data[key] = value
	
	def items(self):
		it = self.data.items()
		it.sort()
		return it

	def clear(self):
		self.data.clear()