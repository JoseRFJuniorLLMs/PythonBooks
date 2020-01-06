# doubletalk - copyright andy robinson 1999
# demodata1.py - some transactions to play with
"""
This script generates a standard set of test data.  It is based on a fictional
startup computer company called 'Pythonics Ltd', which starts in January 1999
and runs for two years.
"""

from doubletalk.transac import *
import doubletalk.bookset
import random
from doubletalk.dates import *
from pprint import pprint


AC_VAT = 'MyCo.Assets.NCA.CurLia.VATdue'
AC_PREPAIDEXPENSE = 'MyCo.Assets.NCA.CurAss.Prepayments'
AC_CREDITORS = 'MyCo.Assets.NCA.CurLia.Creditors'
AC_DEBTORS = 'MyCo.Assets.NCA.CurAss.Debtors'
AC_CASH = 'MyCo.Assets.NCA.CurAss.Cash'
AC_LOAN = 'MyCo.Assets.OtherLia.BankLoan'
AC_EXPENSE = 'MyCo.Capital.PL.Expenses'
AC_INTEREST = 'MyCo.Capital.PL.Expenses.Interest'

AC_INCOME = 'MyCo.Capital.PL.Income'
AC_SHARES = 'MyCo.Capital.Shares'

VAT_RATE = 0.175



# utility to help generate code - assumes I paste rows of numbers
# from Excel into a Python console, and returns lists to paste

def xlRowToList(text):
    print map(eval,string.split(string.strip(text)))

def xlTableToList(text):
    text2 = string.strip(text)
    lines = string.split(text, '\n')
    table = []
    for line in lines:
        if line == '':
            continue
        line = string.strip(line)
        words = string.split(line, '\t')
        row = []
        for word in words:
            if word == '':
                row.append(0)
            else:
                try:
                    num = eval(word)
                    row.append(num)
                except:
                    row.append(word)
        table.append(tuple(row))
    return table
    


#I want repeatable pseudorandom data.  This class has pregenerated numbers
# but behaves like the standard random module.  Some huge limitations - 
# choice becomes useless on lists over 100 items long
class NonRandomGenerator:
    def __init__(self):
        self.ints = getRandInts()   #see hard-coded list at end of module
        self.floats = getRandFloats()   #see hard-coded list at end of module
        self.intpos = 0
        self.floatpos = 0
        
    def choice(self, list):
        nextint = self.ints[self.intpos]
        idx = nextint % len(list)
        self.intpos = self.intpos + 1
        if self.intpos >= len(self.ints):
            self.intpos = 0  # wrap around to start
        return list[idx]
        
    def random(self):
        nextfloat = self.floats[self.floatpos]
        self.floatpos = self.floatpos + 1
        if self.floatpos >= len(self.floats):
            self.floatpos = 0
        return nextfloat
        
    def randint(self, min, max):
        return int(min + (self.random() * (max-min+1)))



def makeMonthlies(startDate, templateTran, amountlist, interval_type=MONTHS, interval_qty=1):
    # supply a 'tempalate transaction' normalised to amount=1; it will be repeated
    # multiplied by the examples each month - look at an example, easier to follow
    # that way
    # if amount is zero, skips
    theDate = startDate
    transactions = []
    for amount in amountlist:
        if amount ==0:
            continue
        newTran = templateTran * amount
        newTran.date = theDate
        newTran.comment = templateTran.comment   # it gets clobbered in derived transactions
        transactions.append(newTran)
        theDate = later(theDate, interval_qty, interval_type)
       
    return transactions        


employeeTable = """
B	Roger, boss	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	
A	Simon, admin	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	
T	Tim, trainee		20	40	60	80	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	
C	Margaret, contractor		140	140	140	140	140	140	140	140	140	140	140	140	140	140	140	140	140	140	140	140	140	140	140	
E	Andy, employee				25	50	75	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	100	
E	Richard, employee								25	50	75	100	100	100	100	100	100	100	100	100	100	100	100	100	100	
"""




def randomCashExpense(maxAmount, startDate=asc2sec('01/01/99'), span=365):
    expense_cats = ['Labour','Rent','Utilities','Travel','Stationery']
    cat = nonrandom.choice(expense_cats)
    amt = int(nonrandom.random()*maxAmount+1)
    time = startDate + nonrandom.randint(1,span)*86400
    t = Transaction()
    t.date = int(time)
    t.comment = 'Random Expense'
    t.addLine(AC_EXPENSE + '.' + cat,amt)
    t.addLastLine(AC_CASH)
    return t
		

def randomExpenses(count=5):
    "return a list of them"
    result = []
    for i in range(count):
        result.append(randomCashExpense())
    return result


class BusinessObject:
	def getTransactions(self):
		return []

def transfer(date, comment, debit, credit, amount):
	# builds two-liners fast
	t = Transaction()
	t.date = date
	t.comment = comment
	t.addLine(debit, amount)
	t.addLine(credit, -amount)
	t.validate()
	return t
	

class Expense(BusinessObject):
	"""Allows for time lags and UK tax"""
	def __init__(self, what, date, amount, category, has_tax=0, payment_lag=0):
		self.what = what
		self.date_received = date
		self.payment_lag = payment_lag
		self.date_paid = self.date_received + 86400 * payment_lag
		self.category = category
		self.net_amount = amount
		self.has_tax = has_tax
		if has_tax:
			self.vat_amount = VAT_RATE * amount
		else:
			self.vat_amount = 0
		self.gross_amount = self.net_amount + self.vat_amount
	
	def getTransactions(self):
		result = []
		if self.payment_lag == 0:
			result.append(self.getCashExpense())
		else:
			result.append(self.getBill())
			result.append(self.payBill())
		return result
		
	def getCashExpense(self):
		t = Transaction()
		t.date = self.date_received
		t.comment = 'Cash Expense - '+ self.what
		t.addLine(AC_EXPENSE + '.' + self.category, self.net_amount)
		if self.has_tax:
			t.addLine(AC_VAT, self.vat_amount)
		t.addLine(AC_CASH, - self.gross_amount)
		return t
		
	def getBill(self):
		t = Transaction()
		t.date = self.date_received
		t.comment = 'Bill received - '+ self.what
		t.addLine(AC_EXPENSE + '.' + self.category, self.net_amount)
		if self.has_tax:
			t.addLine(AC_VAT, self.vat_amount)
		t.addLine(AC_CREDITORS, - self.gross_amount)
		return t
	
	def payBill(self):
		t = Transaction()
		t.date = self.date_paid
		t.comment = 'Bill paid - '+ self.what
		t.addLine(AC_CREDITORS, self.gross_amount)
		t.addLine(AC_CASH, -self.gross_amount)
		return t
	
		
			
def test_expense():
	today = asc2sec('15/2/99')
	exp = Expense('Widgets', today, 100, 'Office', has_tax=1)
	print 'Simple cash expense with tax:'
	exp.getTransactions()[0].display()

	print
	print 'pay one month later...'
	exp = Expense('Widgets', today, 100, 'Office', has_tax=1, payment_lag=30)
	(bill, payment) = exp.getTransactions()
	bill.display()
	payment.display()
	(bill + payment).display()

					
class Income(BusinessObject):
	"""Allows for time lags and UK tax"""
	def __init__(self, what, date, amount, category, has_tax=0, payment_lag=0):
		self.what = what
		self.date_billed = date
		self.payment_lag = payment_lag
		self.date_paid = self.date_billed + 86400 * payment_lag
		self.category = category
		self.net_amount = amount
		self.has_tax = has_tax
		if has_tax:
			self.vat_amount = VAT_RATE * amount
		else:
			self.vat_amount = 0
		self.gross_amount = self.net_amount + self.vat_amount
	
	def getTransactions(self):
		result = []
		if self.payment_lag == 0:
			result.append(self.getCashSale())
		else:
			result.append(self.sendBill())
			result.append(self.getPaid())
		return result
		
	def getCashSale(self):
		t = Transaction()
		
		t.date = self.date_billed
		t.comment = 'Cash Sale - '+ self.what
		t.addLine(AC_INCOME + '.' + self.category, - self.net_amount)
		if self.has_tax:
			t.addLine(AC_VAT, - self.vat_amount)
		t.addLine(AC_CASH, self.gross_amount)
		
		t.validate()
		return t
		
	def sendBill(self):
		t = Transaction()
		
		t.date = self.date_billed
		t.comment = 'Bill raised - '+ self.what
		t.addLine(AC_INCOME + '.' + self.category, - self.net_amount)
		if self.has_tax:
			t.addLine(AC_VAT, - self.vat_amount)
		t.addLine(AC_DEBTORS, self.gross_amount)
		
		t.validate()
		return t
	
	def getPaid(self):
		t = Transaction()
		
		t.date = self.date_paid
		t.comment = 'Payment received - '+ self.what
		t.addLine(AC_DEBTORS, -self.gross_amount)
		t.addLine(AC_CASH, self.gross_amount)
		
		t.validate()
		return t
	
		
			
def test_income():
	today = asc2sec('25/2/99')
	inc = Income('MegaCorp project', today, 100, 'Consulting', has_tax=1)
	print 'Simple cash sale with tax:'
	inc.getTransactions()[0].display()

	print
	print 'pay six weeks later...'
	inc = Income('MegaCorp project', today, 100, 'Office', has_tax=1, payment_lag=45)
	(bill, payment) = inc.getTransactions()
	bill.display()
	payment.display()
	(bill + payment).display()
	
	
class Loan(BusinessObject):
	"""This is a cheat - it assumes you know the payments..."""
	def __init__(self, principal, rate, startdate, pmt):
		self.principal = principal
		self.rate = rate
		self.startdate = startdate
		self.pmt = pmt
		self.outstanding = 0
		
	def getTransactions(self):
		tranlist = []
		
		# draw the money down
		t = Transaction()
		t.date = self.startdate
		t.comment = 'Loan drawdown'
		t.addLine(AC_LOAN, -self.principal)
		t.addLine(AC_CASH, self.principal)
		self.outstanding = self.principal
		t.validate()
		tranlist.append(t)
		
		# pay it back		
		date = self.startdate
		while self.outstanding > 0:
			date = later(date, 1, MONTHS)
			if self.pmt < self.outstanding:
				# a normal one
				interest = 0.01 * int(100 * self.rate * self.outstanding)
				repayment = self.pmt - interest
				
				t = Transaction()
				t.date = date
				t.comment = 'Loan repayment'
				t.addLine(AC_CASH, - self.pmt)
				t.addLine(AC_LOAN, repayment)
				t.addLine(AC_INTEREST, interest)
				t.validate()
				tranlist.append(t)
				
				self.outstanding = self.outstanding - repayment		
			else:
				#final payment to round to zero, waive the interest
				t = Transaction()
				t.date = date
				t.comment = 'Final loan repayment'
				t.addLine(AC_CASH, - self.outstanding)
				t.addLine(AC_LOAN, self.outstanding)
				t.validate()
				tranlist.append(t)
				self.outstanding = 0
				
		return tranlist	
		


def test_loan():
	L = Loan(10000, 0.1, asc2sec('1/3/99'),500)
	for t in L.getTransactions():
		t.display()
			
	
	


def getData():
	# build a list of transactions
	bs = doubletalk.bookset.BookSet()
	
	startDate = asc2sec('1/1/99')
	#make a resuable list of monthly dates to loop over - saves code later
	monthStarts = []
	curDate = startDate
	for i in range(24):
		monthStarts.append(curDate)
		curDate = later(curDate, 1, MONTHS)
	
	monthEnds = []
	curDate = asc2sec('31/1/99')
	for i in range(24):
		monthEnds.append(curDate)
		curDate = later(curDate, 1, MONTHS)
	

	
	# start the company	
	startDate = asc2sec('1/1/99')
	t1 = transfer(startDate, 'Initial investment', AC_CASH, AC_SHARES, 10000)
	bs.add(t1)
	
	# borrow money over 24 months
	L = Loan(10000, 0.1/12.0, asc2sec('1/2/99'),461.45)
	for t in L.getTransactions():
		bs.add(t)
		

	# headcount and staffing levels - 24-item series
	headcounts = [2, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
	
	# office rent - accrue it.  There is not always VAT on rent so we will keep it simple.
	theDate = asc2sec('01/01/99')
	for i in range(24):
		t = Transaction()
		t.date = theDate
		t.comment = 'Monthly Rent Accrual'
		t.addLine(AC_EXPENSE + '.Rent', 1500)
		t.addLastLine(AC_PREPAIDEXPENSE)
		bs.add(t)
		theDate = later(theDate, 1, MONTHS)
	
	# every quarter, actually pay it off in advance
	theDate = asc2sec('01/01/99')
	for i in range(8):
		t = Transaction()
		t.date = theDate
		t.comment = 'Rent paid quarterly in advance'
		t.addLine(AC_PREPAIDEXPENSE, 4500)
		t.addLastLine(AC_CASH)
		bs.add(t)
		theDate = later(theDate, 3, MONTHS)
	

	#regular costs - phone bill paid by direct debit
	template = tranFromTuple((0, 'Phone bills', {}, [
			(AC_EXPENSE + '.Communications', 1.0, None),
			(AC_VAT, 0.175, None),
			(AC_CASH, -1.175, None)])
			)
	for tran in makeMonthlies(startDate, template, [318, 311, 362, 411, 348, 503, 350, 521, 387, 568, 472, 434, 630, 570, 531, 494, 540, 511, 353, 615, 589, 479, 382, 454]):
	    bs.add(tran)
	
	# misc office costs
	template = tranFromTuple((0, 'General office costs', {}, [
			(AC_EXPENSE + '.Office', 1.0, None),
			(AC_VAT, 0.175, None),
			(AC_CASH, -1.175, None)])
			)
	for tran in makeMonthlies(startDate, template, [400, 800, 800, 1000, 1000, 1000, 1000, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200]):
	    bs.add(tran)
	
	# computer hardware - buy on 18th, pay 30 days later
	template = tranFromTuple((0, 'Computer Hardware./Software Investment', {}, [
			('MyCo.Assets.Fixed.Computers.OriginalCost', 1.0, None),
			(AC_VAT, 0.175, None),
			(AC_CREDITORS, -1.175, None)])
			)
	
	for tran in makeMonthlies(startDate + 86400 * 17, template, [8000, 6000, 0, 3000, 0, 0, 0, 3000, 0, 0, 0, 0, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]):
	    bs.add(tran)
		
	template = tranFromTuple((0, 'Computer Hardware./Software Payment', {}, [
			(AC_CASH, -1.175, None),
			(AC_CREDITORS, 1.175, None)])
			)
	
	for tran in makeMonthlies(startDate + 86400 * 47, template, [8000, 6000, 0, 3000, 0, 0, 0, 3000, 0, 0, 0, 0, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]):
	    bs.add(tran)

	#
	#
	#  employee information
	# B=Boss, A = Admin, T  = trainee, E = employee, C = contractor
	#
	employeeInfo = [
		#name, start, monthly wages
		('Roger', asc2sec('1/1/99'), 3000),
		('Simon', asc2sec('1/2/99'), 2000),
		('Tim', asc2sec('1/2/99'), 1500),
		('Andy', asc2sec('1/4/99'), 3000),
		('Richard', asc2sec('1/8/99'), 3000)
		]
	
	for (name, empStartDate, wages) in employeeInfo:
		curDate = empStartDate + (24*86400)   #paid on 25th
		while curDate < monthEnds[-1]:
			t = transfer(curDate, 'Salary for ' + name, AC_EXPENSE + '.Wages', AC_CASH, wages)
			bs.add(t)
			curDate = later(curDate, 1, MONTHS)
	
	# Margaret the contractor is paid weekly, a week in arrears with a lag of a week
	curDate = asc2sec('10/2/99')
	while curDate < monthEnds[-1]:
		exp = Expense('Contractor', curDate, 1500, 'Contractors', has_tax=1, payment_lag=10)
		for tran in exp.getTransactions():
			bs.add(tran)
		curDate = later(curDate, 1, WEEKS)
	

	# consulting sales - bill 5th of following month, paid 35 days later
	# based on an available hours calculation in the spreadsheet
	consultingSales = [4000, 10400, 11200, 13000, 14800, 16600, 17600, 18600, 19600, 20600, 21600, 21600, 21600, 21600, 21600, 21600, 21600, 21600, 21600, 21600, 21600, 21600, 21600, 21600]
	for i in range(24):
		curDate = later(monthStarts[i], 1, MONTHS) + 5 * 86400
		amount = consultingSales[i]
		inc = Income('Consulting to ' + sec2asc(monthEnds[i]), curDate, amount, 'Consulting', has_tax=1, payment_lag=35)
		for tran in inc.getTransactions():
			bs.add(tran)
		
	# software sales - steady flow but take it at the end of the month
	# based on an available hours calculation in the spreadsheet
	productSales = [0, 0, 0, 0, 0, 0, 0, 0, 5000, 5500, 6050, 6655, 7320.5, 8052.55, 17715.61, 19487.17, 21435.888, 23579.48, 25937.42, 42796.75, 47076.43, 51784.07, 56962.48, 62658.7225]
	for i in range(24):
		curDate = monthEnds[i]
		amount = productSales[i]
		inc = Income('Product Sales for month', curDate, amount, 'Software', has_tax=1, payment_lag=0)
		for tran in inc.getTransactions():
			bs.add(tran)
	
	for i in range(484):
	    exp = randomCashExpense(100, asc2sec('1/1/1999'), span=730)  #over 2 years
	    bs.add(exp)
	
	return bs



def getRandInts():
	return [39, 46, 90, 2, 38, 40, 31, 27, 34, 43, 88, 19, 6, 79, 34, 17, 93, 51, 20, 89, 66, 
32, 96, 83, 66, 57, 77, 9, 34, 29, 82, 100, 23, 8, 90, 33, 95, 22, 33, 45, 95, 46, 
39, 41, 20, 82, 83, 31, 40, 0, 55, 30, 52, 23, 64, 81, 10, 12, 60, 47, 60, 8, 33, 
60, 93, 41, 57, 46, 33, 27, 11, 36, 86, 100, 41, 81, 26, 32, 72, 50, 84, 29, 69, 
38, 98, 95, 13, 57, 43, 83, 41, 12, 5, 59, 92, 43, 88, 5, 80, 87, 17, 73, 60, 46, 
81, 66, 45, 45, 73, 15, 41, 48, 46, 0, 10, 49, 95, 35, 61, 24, 59, 52, 1, 11, 42, 
74, 40, 39, 43, 80, 17, 89, 26, 81, 86, 27, 11, 8, 57, 89, 4, 64, 15, 91, 51, 20, 
34, 7, 15, 46, 85, 51, 46, 37, 42, 79, 18, 59, 1, 26, 26, 30, 99, 91, 1, 32, 71, 
84, 61, 87, 32, 3, 72, 78, 65, 7, 90, 47, 63, 13, 47, 49, 97, 53, 24, 54, 96, 49, 
98, 70, 8, 89, 11, 18, 16, 3, 50, 32, 100, 76, 19, 43, 78, 75, 11, 91, 9, 82, 100, 
69, 22, 67, 28, 18, 6, 0, 3, 58, 71, 91, 98, 39, 73, 11, 61, 31, 66, 94, 63, 55, 
26, 31, 62, 2, 30, 7, 68, 2, 64, 86, 42, 47, 81, 52, 3, 96, 83, 16, 99, 50, 60, 43, 
88, 71, 29, 99, 15, 96, 36, 44, 38, 65, 26, 77, 89, 75, 67, 6, 47, 11, 57, 75, 31, 
30, 23, 100, 88, 71, 23, 10, 54, 77, 34, 19, 36, 82, 44, 78, 53, 39, 12, 98, 78, 
5, 98, 87, 69, 47, 63, 82, 73, 34, 61, 8, 67, 9, 40, 47, 51, 97, 62, 7, 77, 20, 1, 
47, 46, 96, 43, 78, 39, 9, 42, 48, 43, 69, 70, 11, 44, 39, 41, 28, 62, 1, 49, 92, 
40, 40, 22, 44, 61, 38, 46, 24, 41, 79, 39, 9, 5, 15, 62, 9, 52, 89, 41, 38, 73, 
6, 63, 74, 59, 61, 26, 67, 74, 94, 74, 53, 31, 59, 34, 60, 55, 87, 53, 19, 13, 36, 
81, 83, 80, 78, 20, 2, 42, 79, 29, 27, 70, 22, 49, 13, 97, 63, 33, 53, 46, 6, 6, 
78, 1, 15, 57, 71, 41, 56, 46, 93, 98, 94, 8, 4, 24, 47, 89, 81, 72, 92, 71, 69, 
80, 17, 90, 55, 14, 81, 42, 93, 93, 6, 16, 26, 89, 69, 69, 6, 32, 13, 50, 6, 19, 
57, 56, 1, 1, 83, 28, 22, 46, 98, 40, 21, 45, 51, 56, 20, 11, 86, 75, 47, 85, 59, 
45, 26, 13, 86, 91, 37, 14, 32, 86, 69, 42, 18, 66, 91, 24, 97, 62, 55, 96, 95, 28, 
60, 26, 3, 84, 100, 52, 93, 25, 32, 32, 99, 59, 23, 0, 71, 12, 87, 44, 89, 94, 78, 
28, 80, 12, 54, 70, 50, 11, 25, 81, 62, 50, 22, 9, 40, 98, 61, 26, 44, 86, 81, 75, 
16, 3, 93, 17, 82, 100, 83, 11, 43, 1, 83, 51, 14, 75, 43, 43, 55, 99, 25, 65, 98, 
52, 91, 78, 23, 58, 65, 94, 88, 52, 28, 9, 69, 61, 40, 22, 76, 79, 27, 34, 40, 79, 
50, 71, 31, 61, 88, 74, 98, 67, 3, 41, 79, 71, 34, 21, 25, 70, 47, 40, 17, 94, 63, 
78, 79, 93, 30, 80, 5, 50, 8, 42, 58, 32, 18, 33, 59, 17, 25, 84, 64, 12, 51, 86, 
0, 78, 79, 58, 71, 42, 3, 38, 4, 29, 95, 54, 29, 83, 74, 25, 32, 87, 53, 5, 59, 85, 
23, 95, 94, 62, 68, 52, 88, 94, 15, 9, 44, 38, 98, 66, 86, 93, 12, 30, 76, 55, 47, 
41, 25, 71, 59, 23, 40, 30, 84, 25, 37, 41, 14, 63, 39, 70, 53, 72, 15, 49, 58, 73, 
2, 40, 90, 64, 80, 1, 10, 73, 93, 15, 82, 28, 28, 43, 49, 81, 47, 78, 44, 81, 72, 
62, 4, 56, 97, 20, 58, 36, 51, 54, 30, 95, 69, 86, 15, 22, 81, 34, 91, 95, 34, 81, 
49, 38, 4, 2, 77, 41, 41, 2, 41, 82, 100, 45, 83, 83, 91, 0, 74, 34, 42, 28, 51, 
58, 8, 16, 66, 46, 11, 4, 33, 24, 15, 89, 75, 63, 68, 76, 40, 47, 14, 78, 78, 71, 
85, 54, 20, 69, 5, 74, 86, 55, 82, 61, 64, 1, 80, 50, 62, 15, 66, 67, 33, 9, 61, 
44, 6, 80, 44, 84, 66, 60, 90, 74, 43, 25, 33, 36, 16, 33, 80, 7, 36, 60, 41, 29, 
90, 12, 70, 35, 69, 7, 70, 9, 0, 27, 60, 93, 7, 83, 80, 95, 96, 0, 59, 20, 0, 18, 
98, 28, 14, 15, 73, 69, 59, 55, 25, 3, 39, 74, 60, 77, 2, 87, 47, 77, 53, 8, 0, 41, 
58, 100, 6, 58, 51, 11, 44, 50, 37, 82, 83, 0, 26, 45, 97, 99, 67, 34, 80, 2, 49, 
16, 95, 22, 30, 23, 66, 68, 76, 57, 52, 72, 31, 56, 43, 86, 5, 58, 57, 96, 25, 81, 
26, 40, 86, 35, 92, 100, 2, 10, 87, 25, 80, 91, 52, 80, 21, 6, 82, 5, 19, 42, 34, 
21, 55, 44, 75, 82, 1, 74, 68, 1, 89, 61, 57, 37, 97, 90, 71, 85, 69, 94, 6, 18, 
30, 48, 94, 38, 7, 20, 76, 34, 81, 91, 15, 81, 53, 42, 33, 85, 88, 65, 93, 78, 9, 
37, 48, 95, 77, 63, 49, 17, 66, 47, 58, 6, 1, 34, 80, 80, 62, 50, 58, 48, 92, 20, 
82, 6, 12, 93, 87, 3, 6, 75, 72, 78, 7, 19, 50, 45, 45, 65, 94, 48, 45, 23, 60, 3, 
85, 100, 44, 48, 63, 78, 63, 7, 4]

def getRandFloats():
	return [0.519063394603, 0.491813174707, 0.361425264847, 0.311398824221, 0.34657818747, 0.0481998280851, 
0.771810981625, 0.55419412997, 0.567077167363, 0.673683025137, 0.273733318084, 0.122761101517, 
0.615323166656, 0.351188678616, 0.198996379924, 0.558083244915, 0.376893848485, 0.0276083843396, 
0.828830460318, 0.645515916907, 0.510058948158, 0.167786363623, 0.0885234527287, 
0.000288268476763, 0.223129018175, 0.982280520319, 0.940089158327, 0.669969071183, 
0.0858013194465, 0.38441698846, 0.697249695985, 0.891317627175, 0.427092321815, 0.303380622324, 
0.0301832483266, 0.0218221917516, 0.706719832096, 0.709931791363, 0.149543340774, 
0.508403980482, 0.924389389643, 0.683386351708, 0.529728212461, 0.656821338954, 0.22508764056, 
0.0398963750458, 0.296460199036, 0.500573708909, 0.183816964979, 0.824799519516, 
0.897846969029, 0.709617087105, 0.691308890572, 0.370367978034, 0.820483033825, 0.593241953627, 
0.62531681972, 0.405317811386, 0.383790343875, 0.706668853712, 0.934221004102, 0.921180765818, 
0.366126592784, 0.393154602279, 0.00765743789232, 0.229229553926, 0.606571986409, 
0.19225861508, 0.859690348602, 0.90584256429, 0.706220938915, 0.100542194919, 0.520096996757, 
0.990750289163, 0.302432298606, 0.338565936874, 0.794052457316, 0.258116683702, 0.771204536826, 
0.164875515771, 0.719936219198, 0.649595456133, 0.171325586347, 0.970860318317, 0.292743423829, 
0.153292963358, 0.0266643256998, 0.342349858678, 0.526006634458, 0.922172566305, 
0.707921375476, 0.554357578832, 0.824966998773, 0.0467730111118, 0.307950941355, 
0.949296522429, 0.843117985843, 0.354801060596, 0.600997163165, 0.106843494397, 0.632589960895, 
0.849344506271, 0.402908592408, 0.601402989072, 0.0773257114608, 0.473464663482, 
0.72279008323, 0.174434930291, 0.149435820153, 0.207375516597, 0.203478330189, 0.0675126384757, 
0.985907742142, 0.217080023707, 0.455980181634, 0.371012614625, 0.637716405843, 0.327312681108, 
0.066482585408, 0.120426550735, 0.291510390236, 0.0732898727041, 0.293991721883, 
0.295136600722, 0.158364562247, 0.637214230375, 0.643842526612, 0.730314864975, 0.13785237437, 
0.424446083164, 0.59232498507, 0.989354628425, 0.000248504730612, 0.579116420171, 
0.00370163577573, 0.181922179633, 0.876695594671, 0.494342374452, 0.281734590052, 
0.869253594419, 0.251338161374, 0.492312837364, 0.412533025392, 0.823117955712, 0.916789249753, 
0.387857584314, 0.0876541223435, 0.24388772919, 0.355360486768, 0.0984319068814, 
0.964408479561, 0.74607240893, 0.366184990163, 0.863189247147, 0.223924740953, 0.784467872649, 
0.0691994822162, 0.0703655025623, 0.522483807681, 0.610638017759, 0.260157344406, 
0.0102799403806, 0.265360838579, 0.48150518794, 0.141780168135, 0.942456298018, 0.440080777104, 
0.121944689243, 0.980037223912, 0.015815131576, 0.61180770986, 0.843434010896, 0.976208471921, 
0.0982514197471, 0.235244735766, 0.277452011274, 0.222963029377, 0.823320983701, 
0.755251971995, 0.146334679675, 0.707548190795, 0.271506898644, 0.992406703868, 0.232380361802, 
0.663746211383, 0.847315796052, 0.632070773133, 0.622810461352, 0.862297006964, 0.327567530298, 
0.843274092004, 0.247417248404, 0.989341812587, 0.787470779141, 0.0687350774711, 
0.38601409904, 0.84130125341, 0.795505555965, 0.40156418045, 0.583145125929, 0.740458281375, 
0.163177059771, 0.183921979854, 0.159145720811, 0.463777731608, 0.593202250775, 0.77246596521, 
0.596347793503, 0.648983645569, 0.83215796595, 0.575106630887, 0.655804630619, 0.0399715441573, 
0.170296196925, 0.36343375545, 0.0381780792306, 0.245931788871, 0.420143136154, 0.828321606026, 
0.91441833198, 0.555176794868, 0.363771571573, 0.632651637634, 0.961900991017, 0.396979992846, 
0.266239814799, 0.133217262784, 0.0948514421673, 0.29765276675, 0.780272471853, 0.588667591038, 
0.664556879181, 0.389420486136, 0.0160451234434, 0.465441493514, 0.268665771753, 
0.625868958711, 0.257176640266, 0.0602146679195, 0.669199043965, 0.63640630106, 0.746082046458, 
0.894334712184, 0.945980962258, 0.534182268834, 0.0278393316702, 0.395117045764, 
0.284654030037, 0.341952976187, 0.0345576280007, 0.465431082948, 0.860955469713, 
0.647006159328, 0.210430814361, 0.0634854363628, 0.833015837528, 0.756714716702, 
0.10058155628, 0.578234223732, 0.270973378515, 0.95142998722, 0.00490020137145, 0.903975519837, 
0.877277163625, 0.705499118946, 0.171904242843, 0.302375001338, 0.149078306815, 0.627686558471, 
0.657666013464, 0.959591610809, 0.392280420589, 0.318535045036, 0.223133340143, 0.730347117728, 
0.931786765418, 0.122798434454, 0.599485023127, 0.510112757128, 0.746854416914, 0.120069364426, 
0.22257345447, 0.414142890766, 0.491633523129, 0.94062283486, 0.483142559832, 0.816800334508, 
0.58614924028, 0.460480813797, 0.387553978089, 0.164613080308, 0.924663211344, 0.556199691697, 
0.0102790420589, 0.367042832149, 0.301316467868, 0.465482589718, 0.551834120994, 
0.419167406566, 0.608009184979, 0.383806567847, 0.910569688999, 0.0877695436676, 
0.223014553551, 0.95433926668, 0.522496706021, 0.17999805929, 0.389931508616, 0.675081855125, 
0.24156658362, 0.533504203092, 0.262705547196, 0.29300693035, 0.612174603631, 0.135828027103, 
0.871224168689, 0.336944741448, 0.894761738197, 0.238575621966, 0.285125941561, 0.420354799117, 
0.477019429602, 0.460124280861, 0.755130443942, 0.588540610533, 0.177805088742, 0.679503075367, 
0.761374314565, 0.772158307693, 0.396549837375, 0.186795618942, 0.106114810474, 0.400483035972, 
0.410929684287, 0.931010825324, 0.233970649611, 0.753946782052, 0.768428379174, 0.091023060479, 
0.688684998951, 0.203499818212, 0.513246257835, 0.426431947067, 0.00241351129794, 
0.593895782345, 0.74311085808, 0.143081495127, 0.897670987028, 0.125133049444, 0.897824446892, 
0.504555736567, 0.133506428376, 0.997910192695, 0.342083474034, 0.293036170189, 0.96092818899, 
0.290747027277, 0.183023454678, 0.362381378698, 0.484419699599, 0.282331447103, 0.959888845781, 
0.618556153849, 0.478748495434, 0.239511352895, 0.605300335603, 0.731282420449, 0.336768814282, 
0.0959436748085, 0.538720375975, 0.534671836861, 0.869620395679, 0.0610819425181, 
0.0658646829903, 0.321629586016, 0.370124422752, 0.932823157111, 0.27893104091, 0.897375154477, 
0.0631629613111, 0.221091597013, 0.306090256752, 0.760302766818, 0.0145435593475, 
0.708903953337, 0.123816738985, 0.423872203991, 0.11730751349, 0.908868849842, 0.7748652583, 
0.972382718505, 0.706108400468, 0.16288814481, 0.808347442321, 0.0550729430228, 0.637658463359, 
0.555584262551, 0.257035692163, 0.719763113075, 0.0896125735457, 0.653686649568, 
0.702973361186, 0.377292442564, 0.717137251795, 0.968629113184, 0.497250844104, 0.951080344997, 
0.376756134328, 0.716429333839, 0.494830302702, 0.975808567089, 0.412348253764, 0.962252288282, 
0.489696750541, 0.281951581072, 0.394312851317, 0.266472432519, 0.971836617865, 0.0865576062114, 
0.773753573847, 0.892042524843, 0.90017158697, 0.853040191289, 0.0635843965394, 0.168850638785, 
0.947997773623, 0.933195148707, 0.416364037961, 0.637940095178, 0.0484709566196, 
0.328939211871, 0.770051840877, 0.552986763159, 0.411546187787, 0.0248143169831, 
0.0103273919003, 0.937222360613, 0.433086890028, 0.52625389546, 0.0120394587035, 
0.905638288733, 0.994499128837, 0.551184980755, 0.974509710948, 0.298751956942, 0.270065593503, 
0.959609230133, 0.320330389322, 0.258743287429, 0.247929690515, 0.469096289476, 0.544962652168, 
0.870895839013, 0.76702445165, 0.818102069042, 0.798313439988, 0.924320608265, 0.594181153911, 
0.695012821082, 0.796544507831, 0.249445108805, 0.393946909124, 0.67186565669, 0.378149260635, 
0.894932334825, 0.248921755383, 0.871731143155, 0.755268623401, 0.187250757713, 0.97047634097, 
0.1711455717, 0.950689772122, 0.995915349579, 0.200705592329, 0.163874027596, 0.355913184408, 
0.215883225488, 0.0246737131611, 0.107878290698, 0.676867202016, 0.48621205776, 0.0507136541121, 
0.606741741323, 0.292629963046, 0.819245196703, 0.16345176556, 0.544040199263, 0.530167387317, 
0.047378824377, 0.719711453168, 0.19002261152, 0.970542739599, 0.779193947977, 0.434796787049, 
0.118951892149, 0.686211437667, 0.655700287327, 0.753335278076, 0.757187110354, 0.0243712629236, 
0.0585554393704, 0.982269777852, 0.593611893803, 0.392518153092, 0.719314288969, 
0.744296286593, 0.602123879846, 0.948115245115, 0.0769505440869, 0.394281810111, 
0.161125744437, 0.267016427564, 0.528702434439, 0.176502455136, 0.529282526252, 0.693856974356, 
0.562638860952, 0.914790534245, 0.107444413554, 0.674052013217, 0.812681023197, 0.0802068021615, 
0.169538409062, 0.695331879748, 0.676014104651, 0.718924445021, 0.710968839745, 0.800669892092, 
0.117176989598, 0.384999240585, 0.991986877605, 0.620955598872, 0.0802397666469, 
0.763456117968, 0.69276172637, 0.532010335986, 0.605227734152, 0.813450992667, 0.473408264135, 
0.190328275116, 0.820030990236, 0.955953990889, 0.634583604879, 0.0978204778019, 
0.431523065223, 0.771117080039, 0.818563400933, 0.577568432325, 0.518828310741, 0.448103376343, 
0.484319456355, 0.238340291499, 0.603071231079, 0.343044420743, 0.358363420897, 0.576004044337, 
0.959559793171, 0.466417656417, 0.0299299661253, 0.612662430502, 0.718128307236, 
0.453918442415, 0.867799134876, 0.808664910535, 0.138202789275, 0.581092958173, 0.574880479214, 
0.751697571477, 0.990038907961, 0.866885097548, 0.444259784771, 0.152105660643, 0.836509322963, 
0.810767516187, 0.0403492895109, 0.626318041298, 0.792414494655, 0.698942948812, 
0.63264543636, 0.0436054539083, 0.148407878915, 0.46323245842, 0.0160567924249, 0.890305635575, 
0.0142449212799, 0.521076854952, 0.509542122951, 0.66743554519, 0.458159706331, 0.251471680682, 
0.742584222207, 0.20497855035, 0.64313549996, 0.614521651535, 0.0681713910681, 0.128826735101, 
0.795886632778, 0.0331819828607, 0.0837319970038, 0.163970497041, 0.220206789454, 
0.480440624748, 0.530079045599, 0.473607672727, 0.708062498857, 0.854950261405, 0.238902174212, 
0.426771520386, 0.462298767688, 0.335103113151, 0.808188119466, 0.0156033319975, 
0.0961750023561, 0.507141294468, 0.784047962046, 0.626751710308, 0.0262928029159, 
0.746822759311, 0.284428756977, 0.19215148054, 0.583754622757, 0.715978678611, 0.262802077018, 
0.199789977166, 0.000660038762554, 0.259397294272, 0.0483231856325, 0.160560436114, 
0.20826458559, 0.018245415249, 0.576908029755, 0.688034140084, 0.24138950384, 0.327072857935, 
0.840106280385, 0.664057789054, 0.231107595508, 0.087000722267, 0.91845994366, 0.514438077543, 
0.854920119824, 0.493679504744, 0.920071313692, 0.238992772723, 0.378413981608, 0.573674540179, 
0.487070880048, 0.0339494086938, 0.232184791015, 0.883844029916, 0.0991954322736, 
0.563732740881, 0.0765268571812, 0.623967566324, 0.260110756788, 0.100945641217, 
0.139629909828, 0.664973217465, 0.760219462711, 0.346336405066, 0.385122903405, 0.96825888068, 
0.844257339775, 0.420424804415, 0.869322492269, 0.926913481433, 0.638014644926, 0.831339391322, 
0.0401307204544, 0.578189151546, 0.474160635411, 0.543154721036, 0.20440964168, 0.387190246765, 
0.737377422966, 0.556576971538, 0.0231229140989, 0.426884379178, 0.724183940613, 
0.85026238276, 0.292231143852, 0.868257045251, 0.239757274656, 0.159465072946, 0.774474159743, 
0.673688121452, 0.923095827095, 0.0564497691467, 0.701369585742, 0.975255447426, 
0.866968506006, 0.379976908716, 0.964218443805, 0.518447989219, 0.536146505316, 0.536411568523, 
0.019409805909, 0.834054210938, 0.501892603821, 0.373350836927, 0.922847010068, 0.433210254373, 
0.37011220427, 0.761849222395, 0.446142638493, 0.759524479972, 0.697470025173, 0.833859896804, 
0.0854197763104, 0.98714286565, 0.0490870410722, 0.333534800685, 0.903898188559, 
0.528827928408, 0.87664663825, 0.974913125833, 0.729192381469, 0.003581470035, 0.248898811237, 
0.586415605965, 0.423120320263, 0.523077175368, 0.864305812511, 0.539030103782, 0.68788514284, 
0.721099547268, 0.343681916717, 0.243942528958, 0.257738642378, 0.424259472742, 0.698416324038, 
0.919540192151, 0.58142927054, 0.925320864329, 0.293495201072, 0.176047034276, 0.660578567316, 
0.424032175564, 0.468685054917, 0.744650550761, 0.854452355907, 0.120432333089, 0.05204654177, 
0.0923839315139, 0.248955582293, 0.401685209347, 0.535849429615, 0.13051206128, 0.283164270074, 
0.0662841232188, 0.794537170419, 0.698654178376, 0.287389056126, 0.722333184724, 
0.0521915348491, 0.0388192619114, 0.38540761928, 0.172721977249, 0.741523564253, 
0.397004729346, 0.528445446631, 0.525855018823, 0.999073344296, 0.841638252242, 0.176832857385, 
0.208905085391, 0.963133174869, 0.87565865882, 0.0276822669036, 0.0718072647835, 
0.813756724794, 0.822127255194, 0.580077575022, 0.106953867963, 0.463360113926, 0.574744123755, 
0.585790947202, 0.91076566713, 0.0778564402169, 0.922148265871, 0.10569043774, 0.844357736083, 
0.9942228201, 0.703297722376, 0.0322302864247, 0.720749265525, 0.182974388789, 0.0201260528591, 
0.602926410382, 0.0665615024438, 0.304816692889, 0.631813416918, 0.165028220973, 
0.380030835737, 0.707345486457, 0.509254097198, 0.866507359577, 0.456464836936, 0.26402032382, 
0.89217817599, 0.739830873104, 0.0591947794168, 0.490145993673, 0.719209508658, 0.632496046264, 
0.548160430588, 0.699801661159, 0.800123173959, 0.541226149896, 0.541808185474, 0.382001646273, 
0.867725686315, 0.794561765591, 0.488959784752, 0.429769600648, 0.551995023626, 0.406690417677, 
0.718744842284, 0.217215700529, 0.0526004796681, 0.349579800995, 0.30643255694, 0.86295827639, 
0.809003964537, 0.635114245883, 0.268112180633, 0.232517139868, 0.578567921182, 0.564450622172, 
0.428013915776, 0.582285352736, 0.16454962057, 0.877681580672, 0.683930415394, 0.557520668835, 
0.274827289801, 0.592473512302, 0.184395372026, 0.0754756210877, 0.448619880621, 
0.505509353448, 0.617593799986, 0.882017505402, 0.899270364228, 0.689770510759, 0.86509104496, 
0.534916622869, 0.0401946506875, 0.492304695593, 0.108170220893, 0.400040136827, 
0.482624664601, 0.696846263717, 0.367044944553, 0.17410224821, 0.590264925841, 0.613053714465, 
0.48186885485, 0.140583378183, 0.714063407895, 0.60843212485, 0.5696638758, 0.95672141642, 
0.705108942063, 0.37035151437, 0.774669400133, 0.344531305173, 0.58135184097, 0.245780976977, 
0.0465656921481, 0.948261470332, 0.338611996954, 0.638621998783, 0.173608209987, 
0.391286834828, 0.00954568864295, 0.427479007286, 0.755444980264, 0.0548400257454, 
0.123966099046, 0.0369920594628, 0.745113906921, 0.679865545517, 0.665878455402, 
0.769423196566, 0.446442546565, 0.595526899984, 0.431986336619, 0.388795910585, 0.0678766097368, 
0.828378882868, 0.791170208833, 0.581702791731, 0.929967960476, 0.63224255358, 0.917768321442, 
0.234962753176, 0.120802912239, 0.887204300686, 0.227129270704, 0.574962333156, 0.713395067949, 
0.564569121524, 0.846083502732, 0.783905253321, 0.196751202553, 0.553736088074, 0.280438988045, 
0.91089762588, 0.211384640105, 0.836566094199, 0.640313992679, 0.88607261343, 0.864825916789, 
0.169855461606, 0.386833188718, 0.561602657777, 0.423429601335, 0.727958756167, 0.104343118441, 
0.473869964568, 0.807438978965, 0.161093459271, 0.256469809844, 0.320962585473, 0.349240804466, 
0.988623964295, 0.82811199436, 0.742017299132, 0.380936444443, 0.275163531159, 0.828464715743, 
0.566793866025, 0.845795630282, 0.318947938287, 0.73789218036, 0.770879937365, 0.532912890939, 
0.671932476013, 0.0387656550378, 0.397331228749, 0.487492172949, 0.219251422884, 
0.724577781263, 0.899513251331, 0.922648302819, 0.106573344633, 0.354892225853, 0.652801986146, 
0.0176827974144, 0.300401274184, 0.978307629158, 0.765623590974, 0.0500257504871, 
0.908658176838, 0.362574252283, 0.441468258111, 0.965175157361, 0.420701432371, 0.673964744841, 
0.366674037612, 0.558346536227, 0.734639061449, 0.450009418089, 0.862079259057, 0.213292141335, 
0.192924729791, 0.335620696225, 0.668630134801, 0.0544902772798, 0.286780241773, 
0.541369521783, 0.352206052753, 0.344589832006, 0.818921540912, 0.349516620351, 0.81023991142, 
0.817523602135, 0.606520162681, 0.306114312417, 0.586551110081, 0.0152160760808, 
0.176024218364, 0.528245365547, 0.7824363983, 0.782706885494, 0.600452193866, 0.707522020843, 
0.827193750802, 0.091098622978, 0.0484813179792, 0.359270060909, 0.186200574367, 
0.161760351356, 0.771621438598, 0.220113986101, 0.969833253555, 0.743220073445, 0.294296125849, 
0.28373581908]

nonrandom = NonRandomGenerator()

if __name__=='__main__':
    #save it with the same name as the module that made it
    import sys
    import os
    filename = os.path.splitext(sys.argv[0])[0] + '.dtj'
    
    bs = getData()
    
    
    bs.save('demodata1.dtj')
    bs.saveAsText('demodata1.log')
    print 'Saved %d transactions in file %s' % (len(bs), filename)
    