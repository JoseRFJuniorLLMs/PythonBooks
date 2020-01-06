
class Magic:
	"Practice at custom methods"
	def __init__(self, value=2):
		print 'Custom object created'
		self.x = value        # ordinary attribute
		self.__list = [1,2,3]   # private attribute
	def __del__(self):
		print 'This object will self-destruct in five seconds'
	def __repr__(self):
		return '<Custom object with value %d>' % self.x
	def __cmp__(self, other):
		return cmp(self.x, other)
	def __hash__(self):
		return hash(self.x)
	def __nonzero__(self):
		return nonzero(self.x)
	
	# setting and getting attributes
	def __getattr__(self, name):
		return 42

	def __setattr__(self, name, value):
		if name == 'spam':
			print 'sorry, I hate spam'
		else:
			self.__dict__[name] = value
	def __call__(self, *args):
		i = 1
		for arg in args:
			print 'argument %d is %s' % (i, arg)
			i = i + 1
	
	# special access stuff
	def __len__(self):
		return len(self.__list)
		
	def __getitem__(self, key):
		return self.__list[key]
		
	def __setitem__(self, key, value):
		self.__list[key] = value
		
	def __delitem__(self, key):
		del(self.__list[key])
		
	# slicing
	
		
