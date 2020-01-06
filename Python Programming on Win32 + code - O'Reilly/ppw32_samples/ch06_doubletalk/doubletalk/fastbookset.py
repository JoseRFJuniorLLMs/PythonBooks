# non-OO bookset written for speedy marshalling

"""
This is intended to go like shit off a shovel compared to the old class-based bookset.
We use lists and dictionaries.  A transaction is a tuple of (date,comment {extrakeys},[lines])
A line is a tuple or list of at least ('account', amount), but perhaps ('account', amount, dict)
Dates are stored as seconds for fast sorting, and converted for display

This means functions instead of method calls for usage, which is less clean to read.
Simple-sounding functions apply to transactions; ones with 'bs_' in the name apply
to booksets.
"""

import string
import marshal
from dtdates import *
import time
import math

#define accounts
VATACCT = "MyCo.Assets.CurLia.VAT"
CURRACCT = "MyCo.Assets.CurAss.Cash.Current"

def new():
	return [int(time.time()),'new transaction',{},[]]

def addline(tran,account,amount):
	tran[3].append((account,amount))

def display(tran):
	print sec2asc(tran[0]),tran[1]
	#now print the optional keys
	dict = tran[2]
	keys = dict.keys()
	keys.sort()
	for key in keys:
		print '    ',key,':',dict[key]
	for line in tran[3]:
		print '%-40s %10.2f' % (line[0],line[1])
	print   #a blank line at the end

def balance(tran):	#should be zero
	sum = 0.00
	for line in tran[3]:
		sum = sum + line[1]
	return sum

def asString(tran):
	"format transaction as readable multi-line text"
	s =  '%-15s %s\n' % ('Date:', sec2asc(tran[0]))
	s = s + '%-15s %s\n' % ('Comment:', tran[1])
	for line in tran[3]:
		s = s + '%-50s\t %10.2f\n' % (line[0], line[1])
	s = s + '\n'
	return s


def tranFromString(chunk):
	chunk = string.strip(chunk) #remove excess newlines
	lines = string.splitfields(chunk,'\n')
	tran = new()
	for line in lines:
		try:
			bits = string.split(line)
			if len(bits) > 2:
				bits = [bits[0],string.join(bits[1:])]
			left = string.strip(bits[0])
			right = string.strip(bits[1])
			if left[-1:] == ':':        #it's a key
				if left == 'Date:':
					tran[0] = asc2sec(right)
				elif left == 'Comment:':
					tran[1] = right
				else:
					tran[2][left[0:-1]]=right
			else:	#it's an account.amount pair
				account = left
				try:
					amount = string.atof(right)
				except:
					amount = 'bollocks'
				tran[3].append((account,amount))
		except:
			pass
			#print 'choked on:'+line
			#print bits

	return tran
	#except:
	#	print "Error with chunk:\n\n"
	#	print chunk

#	far out! accounting algebra!
#	the sum of two transactions is their combined effect at the later of the two dates
#	etc.
#

def add(tran1,tran2):
	newtran = new()
	newtran[0] = max(tran1[0],tran2[0]) #later of two dates
	newtran[1] = 'Sum'
	
	#sum all effects
	numdict = {}
	for line in tran1[3]:
		account = line[0]
		amount = line[1]
		if numdict.has_key(account):
			numdict[account] = numdict[account]+amount
		else:
			numdict[account] = amount
	for line in tran2[3]:
		account = line[0]
		amount = line[1]
		if numdict.has_key(account):
			numdict[account] = numdict[account]+amount
		else:
			numdict[account] = amount
	keys = numdict.keys()
	keys.sort()
	for key in keys:
		newtran[3].append((key,numdict[key]))
	return newtran

def inverse(tran):	#returns the negative
	newtran = (tran[0],'inverse of ('+tran[1]+')',{},[])
	for line in tran[3]:
		newtran[3].append((line[0],0-line[1]))
	return newtran

def subtract(tran1,tran2):   #takes tran2 from tran1
	return add(tran1,inverse(tran2))


##### now some querying stuff - these give true or false

def isBetween(tran, sec1,sec2):
	return (tran[0] >= sec1 and tran[0] <= sec2)
	
def isBeforeOrOn(tran, aDate):
	return (tran[0] <= aDate)

def isOnOrAfter(tran, aDate):
	return (tran[0] >= aDate)

def affects(tran, acct):
	found = 0
	for line in tran[3]:
		if string.find(line[0],acct) <> -1:
			found = 1
	return found




###now for some test crap
def makelots(number):
	data = []
	for i in xrange(number):
		n = new()
		n[1] = 'transaction '+str(i)
		addline(n,'an account',500)
		addline(n,'another account',-500)
		data.append(n)
	return data

def dummypurchase():
	import rand
	n = new()
	n[1] = 'dummy purchase'
	gross = rand.rand()
	net = gross * 40.0/47.0
	vat = gross - net
	addline(n,'MyCo.Capital.PL.Overheads.Acct',net)
	addline(n,'MyCo.Assets.Cash', 0 - gross)
	addline(n,'MyCo.Assets.CurLia.VAT', vat)
	return n




class BookSet:
	"""
a wrapper around the bookset functions above.  Has one
data attribute, journal, which is just a list of transactions.
Access this pulicly.  
"""
	def __init__(self):
		self.journal = []
		
	def list(self):
		for tran in self.journal:
			display(tran)

	def save(self, filename):
		f = open(filename,'wb')
		marshal.dump(self.journal,f)
		f.close()

	def saveAsText(self, filename):
		f = open(filename,'w')
		for tran in self.journal:
			f.write(asString(tran))
		f.close()

	def loadFromText(self, filename):
		chunks = self.readChunks(filename)
		self.journal = map(tranFromString,chunks)
	
	def readChunks(self, filename):
		#loads a doubletalk file. private utility, do not call
		f = open(filename,'r')
		bigstring = f.read()  #read in up to 100MB - should do for now
		f.close()
		chunks = string.splitfields(bigstring,'\n\n')
		if chunks[-1] == '':
			chunks = chunks[:-1]
		return chunks	


	def load(self, filename):
		f = open(filename,'r')
		self.journal = marshal.load(f)
		f.close()

	def listAccount(self, match):
		runtot = 0
		tranNo = 0
		print
		print 'Details of account',match
		print '---------------------------'
		for tran in self.journal:
			dateStr = sec2asc(tran[0])
			comment = tran[1]
			for line in tran[3]:
				account = line[0]
				if string.find(account,match)<> -1:
					delta = line[1]
					runtot = runtot + delta
					print '%5d %-15s %-30s %10.2f %10.2f' % (tranNo, dateStr, comment, delta, runtot) 
			tranNo = tranNo + 1
	
		print

	def acctList(self, dimension=0):
		"""
		gathers a list of all accounts.  If you are putting job/project info in
		another dimension, specify that.
		"""
		uniqueDict = {}
		for tran in self.journal:
			for line in tran[3]:
				uniqueDict[line[dimension]]=1
		list = uniqueDict.keys()
		list.sort()
		return list
	
	def BalanceOn(self, date):
		accts = {}
		for tran in self.journal:
			if tran[0] > date:
				break
			for line in tran[3]:
				account = line[0]
				amount = line[1]
				if accts.has_key(account):
					accts[account]=accts[account] + amount
				else:
					accts[account] = amount
		items = accts.items()
		items.sort()
		return items
	
	def PrintBalanceOn(self, date):
		bals = self.BalanceOn(date)
		print 'Balance On',time.ctime(date)
		print '_' * 20
		
		for bal in bals:
			print bal[0],'\t',bal[1]
			
	
		

	def matchAcct(self,stub):
		acctlist = self.acctList(self.journal)
		result = '(uncategorised)'
		for acct in acctlist:
			if string.find(acct,stub)<> -1:
				result = acct
				break
		return result


	def map(self,mapping):
		for tran in self.journal:
			lines = tran[3]
			for i in range(len(lines)):
				line = lines[i]
				acct = line[0]
				amt = line[1]
				if mapping.has_key(acct):
					lines[i] = (mapping[acct],amt)
					#print 'mapped',acct, mapping[acct]


	def compact(self):	#adds up identicals
		for i in range(len(self.journal)):
			tran = self.journal[i]
			accts = {}
			for line in tran[3]:
				account = line[0]
				amount = line[1]
				if accts.has_key(account):
					accts[account]=accts[account] + amount
				else:
					accts[account] = amount
			keys = accts.keys()
			keys.sort()
			newlines = []
			for key in keys:
				if accts[key] <> 0:
					newlines.append((key,accts[key]))
						
			# make a new transaction and swap it in
			newtran = (tran[0], tran[1], tran[2], newlines)
			self.journal[i] = newtran

	def all_balances(self):
		return map(balance,self.journal)
	
	def checksum(self):	
		"does it add up to zero? If not, list offenders"
		total = 0
		for tran in self.journal:
			b = balance(tran)
			if abs(b)>=0.01:
				print 'Error:',b
				display(tran)
				print '_' * 20
			total = total + b
		return total
		
	def sum(self):
		total = (0,'blank',{},[])
		for tran in self.journal:
			total = add(total,tran)
		return total

	def help(self):
		print self.__doc__		

def dp2(aFloat):
	return int(100*aFloat)/100.0



###### transaction-making stuff #######


def transfer(date, comment, debit, credit, amount):
	return (date, comment, {}, [
			(debit, amount),
			(credit, - amount)])

def cashPurchase(dateStr,comment,payee,account,net,hasVAT=1):
	tran = new()
	tran[0] = asc2sec(dateStr)
	tran[1] = comment
	tran[2]['Customer']=payee	#use an extra key
	if hasVAT:
		vat = 0.175 * net
		gross = 0 - net - vat
		addline(tran, 'MyCo.Capital.PL.Costs.'+account,net)
		addline(tran, VATACCT, vat)
		addline(tran, CURRACCT, gross)
	else:
		addline(tran, 'MyCo.Capital.PL.Costs.'+account,net)
		addline(tran, CURRACCT, 0 - net)
	return tran

eg1 = cashPurchase('30/09/96','laptop','Gateway','MyCo.Assets.Fixed.Computers',2000)
eg2 = cashPurchase('31/10/96','train pass','London Undergrounf','MyCo.Capital.PL.Overheads.Travel',70,0)





def test():
	print 'alive and well'