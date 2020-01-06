# non-OO bookset written for speedy marshalling

"""
slow bookset for OO transactions - much slower than fastran/fastbookset
which works with a list of tuple-structures.
"""

import string
import marshal
from doubletalk.dates import *
import time
import math
import cPickle
import doubletalk.transac
import doubletalk.datastruct


class BookSet:
	"""
a wrapper around a list of transactions.  Has one
data attribute, journal, which is just a list of transactions
guaranteed to be in order.
Hides its innards  
"""
	def __init__(self):
		self.__journal = []
	
	def _clear(self):
		# subclasses might need a more sophisticated clear method
		self.__journal = []
		
	############################################	
	#
	#     Utilities 
	#
	############################################
	

	def __len__(self):
		return len(self.__journal)

	def __getitem__(self, i): 
		return self.__journal[i]
	
	def __getslice__(self, i, j):
		# returns a smaller bookset
		bs2 = BookSet()
		for tran in self.__journal[i:j]:
			bs2.add(tran)
		return bs2

	#def sort(self):
	#	"This should not be necessary at all, but just in case"
	#	self.__journal.sort()
		
	def list(self):
		for tran in self.__journal:
			tran.display()

	def isEqual(self, other):
		if len(self) <> len(other):
			print 'lengths differ:  %d, %d' % (len(self), len(other))
			return 0
		else:
			for i in range(len(self)):
				t1 = self[i]
				t2 = other[i]
				if not t1.isEqual(t2):
					print 'difference at position',i
					print 'self:', t1.asTuple()
					t1.display()
					print 'other:', t2.asTuple()
					t2.display()
					return 0
			return 1

	def matchAccount(self, stub):
		"finds a full account name matching a partial name your supply"
		acctlist = self.getAccountList()
		result = '(uncategorised)'
		for acct in acctlist:
			if string.find(acct,stub)<> -1:
				result = acct
				break
		return result


	######################################
	#
	# add / edit / delete / rename
	# basic operations to modify it
	#
	######################################
	
	def add(self, tran):
		# this could be optimised by putting the
		# length=0 case in an exception handler
		tran.validate()
		if len(self.__journal) == 0:
			self.__journal.append(tran)
		else:
			# quick check if it is the last - might happen
			# very often when loading from a file
			if cmp(tran, self.__journal[-1]) >= 0:
				self.__journal.append(tran)
			else:
				self._insertInOrder(tran)

	def _insertInOrder(self, tran):
		# copied from Python library - binary
		# insertion routine
		lo = 0
		hi = len(self.__journal)
		while lo < hi:		
			mid = (lo + hi) / 2
			if tran < self.__journal[mid]:
				hi = mid
			else:
				lo = mid + 1
		self.__journal.insert(lo, tran)

	def remove(self, index):
		# removes the transaction at 'index'
		tran = self.__journal[index]
		del self.__journal[index]
		return tran
	
	def edit(self, index, newTran):
		newTran.validate()
		del self.__journal[index]
		self.add(newTran)
	
	def renameAccount(self, oldAcct, newAcct, compact=1):
		"""This may be used to 'lose detail'.  If compact is false,
		one might end up with several lines in the same transaction
		which all worked on the same account.  compact=1 tidies these up"""
		
		for tran in self.__journal:
			tran.renameAccount(oldAcct, newAcct)
			if compact:
				tran.compact()
		

	######################################
	#
	# save functionality.  See below for load
	#
	######################################
	
	def save(self, filename):
		f = open(filename,'wb')
		cPickle.dump(self.__journal,f)
		f.close()

	def saveAsText(self, filename):
		f = open(filename,'w')
		for tran in self.__journal:
			f.write(tran.asString())
		f.close()

	def asString(self):
		chunks = []
		for tran in self.__bookset:
			chunks.append(tran.asString())
		return string.join(chunks, '\n')
	
	def load(self, filename):
		self._clear()
		f = open(filename, 'r')
		data = cPickle.load(f)
		for tran in data:
			self.add(tran)
		f.close()
		
	def loadFromText(self, filename):
		self._clear()
		chunks = self._readChunks(filename)
		for chunk in chunks:
			tran = doubletalk.transac.tranFromString(chunk)
			self.add(tran)
	
	def loadFromString(self, bigstring):
		self._clear()
		chunks = string.splitfields(bigstring,'\n\n')
		if chunks[-1] == '':
			chunks = chunks[:-1]
		for chunk in chunks:
			tran = doubletalk.transac.Transaction()
			tran.fromString(chunk)
			self.add(tran)
	
	def _readChunks(self, filename):
		#loads a doubletalk file. private utility, do not call
		# loads whole file
		f = open(filename,'r')
		bigstring = f.read() 
		f.close()
		chunks = string.splitfields(bigstring,'\n\n')
		if chunks[-1] == '':
			chunks = chunks[:-1]
		return chunks	

	# loading is done in functions
	
	################################################################
	#
	#     find
	#
	#
	################################################################

	def findLastOnOrBefore(self, date):
		# binary search 
		lo = 0
		hi = len(self.__journal)
		while lo < hi:		
			mid = (lo + hi) / 2
			if date < self.__journal[mid].date:
				hi = mid
			else:
				lo = mid + 1
		return lo - 1
	
	def findFirstAfter(self, date):
		# binary search 
		lo = 0
		hi = len(self.__journal)
		while lo < hi:		
			mid = (lo + hi) / 2
			if date < self.__journal[mid].date:
				hi = mid
			else:
				lo = mid + 1
		return lo
		
	################################################################
	#
	#     basic query and command-line display functionality
	#
	# getBlahBlah generally returns some list or tuple structure
	# displayBlahBlah calls it and prints from the command line
	#
	################################################################


	def getAccountDetails(self, match):
		from string import find  # import into local namespace, a bit faster
		runtot = 0
		tranNo = 0
		results = []
		for tran in self.__journal:
			dateStr = sec2asc(tran.date)
			comment = tran.comment
			for (account, delta, etc) in tran.lines:
				if find(account,match)<> -1:
					runtot = runtot + delta
					results.append((tranNo, dateStr, comment, delta, runtot)) 
			tranNo = tranNo + 1
		return results
		
	def listAccountDetails(self, match):
		print 'Details of account',match
		print '------------------ ' + ('-' * len(match))
		for row in self.getAccountDetails(match):
			print '%5d %-12s %-40s %10.2f %10.2f' % row
		print

	def getAccountList(self):
		"gathers a list of all accounts"
		acSet = doubletalk.datastruct.Set()
		for tran in self.__journal:
			for line in tran.lines:
				acSet.add(line[0])
		return acSet.elements()
		
	def listAccountList(self):
		"displays accounts in alpha order, one per line"
		print 'List of Accounts Used:'
		print '---------------------'
		for acct in self.getAccountList():
			print acct
		print			
	
	def getAllBalancesOn(self, date=LATE):
		"returns direct balances of all accounts"
		numdict = doubletalk.datastruct.NumDict()
		for tran in self.__journal:
			if tran.date > date:
				break
			for (account, amount, etc) in tran.lines:
				numdict.inc(account, amount)
		return numdict.items()
	
	def listAllBalancesOn(self, date=LATE):
		"prints direct balances of all accounts"
		bals = self.getAllBalancesOn(date)
		
		header = 'Account Balances On ' + time.ctime(date) + ':'
		print header
		print '_' * (len(header)+1)
		
		for bal in bals:
			print '%-50s  %10.2f' % bal
			
	
	def getAccountBalance(self, acct, date=LATE):
		"as it says"
		total = 0
		for tran in self.__journal:
			if tran.date > date:
				break
			total = total + tran.effectOn(acct)
		return total

	def getAccountActivity(self, acct, startDate=EARLY, endDate=LATE):
		"as it says"
		total = 0
		for tran in self.__journal:
			# could speed this up by seeking to right position intelligently
			if tran.date < startDate:
				continue
			if tran.date > endDate:
				break
			total = total + tran.effectOn(acct)
		return total
	

	def getMonthlyActivity(self, startDate=EARLY, endDate=LATE):
		"""Return a table with monthly activities per account.
		This will be generalized out in a query language but
		is included here as an example.  Request a range outside
		the bookset (i.e. both before or both after) will cause an
		error"""
		
		acctlist = self.getAccountList()
		
			
		# make a list of dates as 199901
		startidx = self.findFirstAfter(startDate)
		endidx = self.findLastOnOrBefore(endDate)
		
		thisperiod = yyyymm(self.__journal[startidx].date)
		lastperiod = yyyymm(self.__journal[endidx].date)

		months = []
		while thisperiod <= lastperiod:
			months.append(thisperiod)
			(year, month) = divmod(thisperiod, 100)
			month = month + 1
			if month > 12:
				year = year + 1
				month = 1
			thisperiod = year * 100 + month
			
		monthcount = len(months)		
		
		# build a sparse matrix
		matrix = doubletalk.datastruct.NumDict()
		for tran in self.__journal:
			monthend = yyyymm(tran.date)
			for (account, amount, etc) in tran.lines:
				index = (monthend, account)
				matrix.inc(index, amount)


		# now make a table
		table = []
		#header row - one extra item at the beginning
		table.append([None] + months[:])
		
		#the body
		for acct in acctlist:
			row = [acct]
			for monthend in months:
				index = (monthend, acct)
				value = matrix[index]
				row.append(value)
			table.append(row)
			
		# check it balances - debug code
		for colnum in range(1, len(row)):
			coltotal = 0.0
			for rownum in range(1, len(table)):
				coltotal = coltotal + table[rownum][colnum]
			assert abs(coltotal) < 0.0001, 'Column %d sums to %f' % (table[0][colnum], table[rownum][colnum])

		return table
		

		
		

	########################################################################
	#
	#
	#  More utilities for querying and transforming
	#
	########################################################################
	


	def map(self,mapping):
		""""Does lots of renaming operations based on a dictionary.
		Allows massive restructuring of the balance tree.  for example,
		you could prepare and save a dictionary to map from your accounting
		system's representation to that of your spreadsheet."""
		for tran in self.__journal:
			for i in range(len(tran.lines)):
				(account, amount, etc) = tran.lines[i]
				if mapping.has_key(account):
					tran.lines[i] = (mapping[acct], amount, etc)
					#print 'mapped',acct, mapping[acct]


	def compact(self):	
		"adds up identical lines within each transaction"
		for tran in self.__journal:
			tran.compact()

	def validate(self):
		""""check the double-entry rule. We validate on adding but
		something might have crept in if the programmer is using
		direct access.  this causes an exception if any transaction
		fails to balance"""
		for tran in self.__journal:
			tran.validate()

	#def getTimeSlice(self, startdate, enddate):
	#	bs2 = BookSet()
	#	length = len(self.__journal)
	#	pos = self.findFirstAfter(startdate)
	#	tran = self.__journal[pos]
	#	while tran.date < enddate and pos < length:
	#		bs2.__journal.append(tran.copy() 
		
	def sum(self):
		total = doubletalk.transac.Transaction()
		for tran in self.__journal:
			total = total + tran
		return total

	def help(self):
		print self.__doc__		

def dp2(aFloat):
	return int(100*aFloat)/100.0



######################################
#
# load functionality - effectively makes a new one
# so put this outside the class
#
######################################


def loadBookSet(filename):
	B = BookSet()
	f = open(filename, 'r')
	data = cPickle.load(f)
	for tran in data:
		B.add(tran)
	f.close()
	return B

def loadBookSetFromText(filename):
	B = BookSet()
	B.loadFromText(filename)
	return B
	


###### transaction-making stuff #######


def transfer(date, comment, debit, credit, amount):
	return (date, comment, {}, [
			(debit, amount),
			(credit, - amount)])


def test():
	import tempfile
	import os
	try:
		import demodata1
	except:
		print 'demodata1 not available, cannot test'
		return
	
	
	B = demodata1.getData()
	print 'Bookset created'
	

	filename = tempfile.mktemp()
	B.save(filename)
	B2 = loadBookSet(filename)
	os.remove(filename)
	if B.isEqual(B2):
		print 'passed save-load test'
	else:
		print 'failed save-load test'
		return
		
	# now for tuple conversion
	list = []
	for tran in B:
		list.append(tran.asTuple())
	B3 = BookSet()
	for trantuple in list:
		B3.add(doubletalk.transac.tranFromTuple(trantuple))
	if B.isEqual(B3):
		print 'passed tuple-conversion test'
	else:
		print 'failed tuple-conversion test'
		return
	
	# now try saving as text
	filename = tempfile.mktemp()
	B.saveAsText(filename)
	B4 = BookSet()
	B4.loadFromText(filename)
	#if B.isEqual(B4):
	#	print 'passed text save-load test'
	#else:
	#	print 'failed text save-load test'
	#	#return
	
	##############################################
	#
	#     now for add/edit/delete/rename
	#
	##############################################
	B[1].comment = 'unlikely'
	pulled = B.remove(1)
	pulled = pulled * 1.5
	B.add(pulled)
	
	B.renameAccount('MyCo.Capital.PL.Expenses','MyCo.Capital.PL.Costs')
	B.renameAccount('MyCo.Assets.Cash','MyCo.Assets.CurAss.Cash')
	print 'renamed'
	for i in range(5):
		B[i].display()
	print 'Cash account follows...\n\n'
	B.listAccountDetails(demodata1.AC_PREPAIDEXPENSE)


	return B
	
if __name__ == '__main__':
	test()
	