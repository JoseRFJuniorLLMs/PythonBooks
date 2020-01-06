# part of DoubleTalk - copyright andy robinson 1998
""" 
Transaction classes and operations

This defines a class to represent an accounting transaction.  My first ever
implementations used classes, which were quite slow when looping over thousands
or tens of thousands, but made for very readable code.   I then used a tuple
based structure which was much faster.  At this stage the main need is to
'sell' the idea of an algebra of transactions, and I have graduated from
25Mhz to 233 MHz, so I am reverting to classes.  I believe we could easily
create an extension module in the future to alleviate these problems.

Transactions are an abstraction going back 400 years which has served the world
very well. They should NOT be subclassed as their behaviour should be a guaranteed
standard everywhere.  Extra behaviour can be gained through many other design
patterns, and extra analytics added as functions.

They can be extended at the 'transaction' level with ordinary attributes, and
at the line level with an optional extra dictionary
"""

import time
from dates import *
import datastruct

DoubletalkError = 'DoubletalkError'
ERROR_ACCOUNT_NAME = '(uncategorised)'
ROUNDING_THRESHOLD = 0.0001    #100 times smaller than cents or pennies

class Transaction:
	"""
	a double-entry bookkeeping transaction.  As text, this could 
	go like:
		28/9/98   Start the Company
		MyCo.Assets.Cash            +10000
		MyCo.Capital.ShareCapital   -10000
	"""
	def __init__(self):
		"By default, you get a zero transaction with time = now"
		import time
		self.date = int(time.time())
		self.comment = '<New Transaction>'
		self.lines = []
	
	def __cmp__(self, other):
		"Allow python's native list sort to work - date order"
		return cmp(self.date, other.date)
		
	def __str__(self):
		"return a string suitable for printing in a listing"
		return self.asString()	
	
	def getDateString(self):
		# allows us to treat dates with strings, which are system-independent
		return sec2asc(self.date)
			
	def setDateString(self, aDateString):
		self.date = asc2sec(aDateString)
		
	def isEqual(self, other):
		# the obvious one below is too fascist 
		# - need several notions of comparison
		# return self.asTuple() == other.asTuple()
		# the one we will use is 'nearly same numbers, same dates'
		self.lines.sort()
		other.lines.sort()
		if int(self.date) <> int(other.date):
			return 0
		count = len(self.lines)
		if count <> len(other.lines):
			return 0
		for i in range(count):
			(ac1, amt1, etc1) = self.lines[i]
			(ac2, amt2, etc2) = other.lines[i]
			
			# round off and compare
			cmp1 = (ac1, int(amt1*100), etc1)
			cmp2 = (ac2, int(amt2*100), etc2)
			return cmp1 == cmp2
		
	
	def addLine(self, account, amount, dict = None):
		"add a line - used for building transactions"
		self.lines.append((account, amount, dict))
	
	def addLastLine(self, account, dict = None):
		"adds the final line, the balance being calculated to total zero"
		neededAmount = 0 - self.balance()
		self.lines.append((account, neededAmount, dict))
	
	def balance(self):
		"sum of lines - should be zero"
		bal = 0
		for line in self.lines:
			bal = bal + line[1]
		if abs(bal) < ROUNDING_THRESHOLD:
			bal = 0
		return bal
		
	def validate(self, autocorrect=0):
		"""Used when building transactions.  Checks it balances,
		and if not adds a line with the account 'Uncategorised'"""
		
		# currently worrying about rounding errors, precision to
		# nearest second
		self.date = int(self.date)
		
		amountNeeded = 0 - self.balance()
		
		if amountNeeded <> 0:
			if autocorrect:
				self.addLine(ERROR_ACCOUNT_NAME, amountNeeded, None)		
			else:
				raise DoubletalkError, 'Transaction does not balance'

	def renameAccount(self, oldAcct, newAcct):
		matchlen = len(oldAcct)
		for i in range(len(self.lines)):
			(account, amount, etc) = self.lines[i]
			if account[0:matchlen] == oldAcct:
				self.lines[i] =(newAcct + account[matchlen:], amount, etc)
		

	def compact(self):
		"compacts identical accounts together.  Line dictionary set to None"
		nd = datastruct.NumDict()
		for line in self.lines:
			(account, amount, etc) = line
			nd.inc(account,amount)
		#now read the compacted amount back
		self.lines = []
		for item in nd.items():
			if item[1] <> 0:
				self.lines.append((item[0],item[1],None))
		self.lines.sort()

	##################################################################
	#
	#   eases querying in booksets
	#
	##################################################################

	def effectOn(self, targetAccount):
		
		effect = 0
		cutoff = len(targetAccount)
		for (account, amount, etc) in self.lines:
			if account[0:cutoff] == targetAccount:
				effect = effect + amount
		return effect

        def flows(self, fromAccount):
            nd = datastruct.NumDict()
            matchlen = len(fromAccount)
            for (account, amount) in self.lines:
                if account[0:matchlen] <> fromAccount:
                    nd.inc(account, amount)
            return nd.items()
            
	#
	#
	# magic methods for transaction maths
	#


	def __add__(self, other):
		"""take date of latter, and compact the amounts.  Not yet sure what
		to do to the keys, so assume the worst and set to None for now"""

		nd = datastruct.NumDict()
		
		# take data from the first:
		for line in self.lines:
			(account, amount, etc) = line
			nd.inc(account,amount)
		# ...and the second
		for line in other.lines:
			(account, amount, etc) = line
			nd.inc(account,amount)
		
		# now read the compacted amount back into a new one
		newtran = Transaction()
		for item in nd.items():
			newtran.lines.append((item[0],item[1],None))
			
		newtran.date = max(self.date, other.date)
		newtran.comment = '<derived transaction>'

		newtran.compact()
		
		return newtran
	
	def __neg__(self):
		t = Transaction()
		t.date = self.date
		for line in self.lines:
			(account, amount, etc) = line
			t.addLine(account, -amount, etc)
		return t
			
	def __mul__(self, scalar):
		t = Transaction()
		t.date = self.date
		for line in self.lines:
			(account, amount, etc) = line
			t.addLine(account, scalar * amount, etc)
		return t
	
	def __div__(self, scalar):
		return self * (1.0/scalar)
	
		
	def display(self):
		print self.asString()
		

	################################################
	#
	#	conversions
	#
	################################################
	
	def asTuple(self):
		# returns a high-speed version - nominal ledger only
		
		return (self.date, self.comment, {}, self.lines[:])
		

	def asString(self):
		self.lines.sort()
		s = 'Date:\t' + sec2asc(self.date) + '\n'
		s = s + 'Comment:\t ' + self.comment + '\n'
		for line in self.lines:
			s = s + '%-40s %10.6f\n' % line[0:2]
		s = s + '\n'
		return s
	
	def asDicts(self):
		# returns a list of dictionaries with denormalized
		# data.  Each is guaranteed to contain the keys
		# 'Date', 'Comment', Account' and 'Amount', and will
		# contain any other stuff found.  Line attributes
		# take priority over transaction attributes.  Useful
		# for building a 'data warehouse'.
		dicts = []
		i = 0
		for line in self.lines:
			rowdict = self.__dict__.copy()
			del rowdict['lines']
			rowdict['account'] = line[0]
			rowdict['amount'] = line[1]
			if line[2]:
				rowdict.update(line[2])
			i = i + 1
			dicts.append(rowdict)
		return dicts
		
	################################################
	#
	#	miscellaneous
	#
	################################################
	
	def magnitude(self):
		"""A somewhat artificial measure which is useful if you
		need a one-line description.  Take absolute values of all
		lines, sum and halve. Gives a notion of th 'size' of the 
		transaction.  For a two-liner this is obvious; for a 
		multi-line invoice it will give the invoice total.  May not
		make sense for huge 'opening balance' type transactions."""
		tot = 0
		for (account, amount, etc) in self.lines:
			tot = tot + abs(amount)
		return 0.5 * tot


def tranFromString(chunk):
	chunk = string.strip(chunk) #remove excess newlines
	lines = string.splitfields(chunk,'\n')
	tran = Transaction()
	for line in lines:
		try:
			bits = string.split(line)
			if len(bits) > 2:
				bits = [bits[0],string.join(bits[1:])]
			left = string.strip(bits[0])
			right = string.strip(bits[1])
			if left[-1:] == ':':        #it's a key
				if left == 'Date:':
					tran.date = asc2sec(right)
				elif left == 'Comment:':
					tran.comment = right
				else:
					setattr(tran, left, right)
			else:	#it's an account.amount pair
				account = left
				try:
					amount = string.atof(right)
				except:
					amount = 'bollocks'
				tran.addLine(account, amount)
		except:
			pass
			#print 'choked on:'+line
			#print bits

	return tran

def tranFromTuple(tuple):
	tran = Transaction()
	tran.date = tuple[0]
	tran.comment = tuple[1]
	if tuple[2] <> None:
		for (key, value) in tuple[2].items():
			tran.__dict__[key] = value
	for (account, amount, etc) in tuple[3]:
		tran.addLine(account, amount, etc)
	return tran
		


def sample():
	t = Transaction()
	t.comment = 'Start the company'
	t.addLine('MyCo.Assets.Cash',10000)
	t.addLine('MyCo.Capital.Shares',-10000)
	return t
	

def sample2():
	t = Transaction()
	t.comment = 'Start the company'
	t.customer = 'Smiths'
	t.addLine('MyCo.Assets.Cash',10000, {'bank':'NatWest'})
	t.addLine('MyCo.Capital.Shares',-10000)
	return t
