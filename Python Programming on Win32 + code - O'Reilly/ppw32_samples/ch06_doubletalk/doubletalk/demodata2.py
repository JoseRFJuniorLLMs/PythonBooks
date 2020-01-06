# doubletalk - copyright andy robinson 1998
# demodata2.py - makes transactions to play with


from doubletalk.bookset import *
import random
import time


demodir = 'd:\\data\\project\\doubletalk\\demodata\\'

def getStartTran():
	tran = (time.time(),'<Start a company>',{},
		[
		('MyCo.Assets.Cash',10000, None),
		('MyCo.Capital.ShareCapital',-10000,None)
		])
	return tran

	
def randomCashExpense():
	expense_cats = ['Labour','Rent','Utilities','Travel','Stationery']
	cat = random.choice(expense_cats)
	amt = 0.01 * int(random.random()*100000)
	dat = asc2sec('01/01/1998') + 0.5 + random.randint(1,365)*86400
	tran = (dat,'Random Expense',{},[
			('MyCo.Capital.PL.Expenses.' + cat,amt,None),
			('MyCo.Assets.Cash',0 - amt, None)
			])
	return tran
		

def randomBookSet(count=10):
	B = BookSet()
	
	# put in some capital
	B.journal.append(getStartTran())
	
	#fritter it away
	for i in range(count):
		B.journal.append(randomCashExpense())
	return B