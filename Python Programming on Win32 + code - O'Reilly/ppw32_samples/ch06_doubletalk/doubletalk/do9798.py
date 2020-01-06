# make 97/98 accounts


import dbi, odbc
from bookset import *
from time import *
from pprint import pprint
import os

WORKDIR = 'c:\\data\\robanal\\accounting\\9798\\'

def roundtime(secs):
	# I get a lot of 23:00 ones due to time zone
	return int((43200 + secs) / 86400.0) * 86400
	
def ymd2time(y,m,d):
	try:
		return mktime((y,m,d,0,0,0,0,0,0))
	except:
		print 'Error converting date:',y,m,d
		raise AccountsError

def ddmmyyyy(secs):
	try:
		bits = gmtime(secs)
		return str(bits[2])+'-'+str(bits[1])+'-'+str(bits[0])
	except:
		print 'tried to convert time',secs

AccountsError = 'Accounts Error'	
	


class RawData:
	def __init__(self):
		self.fetch()
	
	def _fetchtable(self, tablename, order=None):	
		cursor = self._conn.cursor()
		stmt = 'SELECT * FROM '+tablename
		if order <> None:
			stmt = stmt + ' ORDER BY ' + order
		cursor.execute(stmt)
		result = cursor.fetchall()
		cursor.close()
		return result

	def _fetchdicts(self, tablename, order=None):
		cursor = self._conn.cursor()
		stmt = 'SELECT * FROM '+tablename
		if order <> None:
			stmt = stmt + ' ORDER BY ' + order
		cursor.execute(stmt)
		fieldlist = map(lambda x:x[0], cursor.description)
		fieldcount = len(fieldlist)
		data = cursor.fetchall()
		cursor.close()
		
		dicts = []
		for row in data:
			dict = {}
			for i in range(fieldcount):
				dict[fieldlist[i]] = row[i]
			dicts.append(dict)
		return dicts

	def fetch(self):
		self._conn = odbc.odbc('AndyAccounts')
		self.drawings = self._fetchtable('Drawings')
		self.sales = self._fetchtable('Sales','SaleID')
		
		# new feature added later		
		self.expenses = self._fetchdicts('Expenses', 'ExpenseID')

		self._conn.close()
		
				
	def doDrawings(self):
		output = []
		for row in self.drawings:
			date = roundtime(row[1].value)
			tran = (date, 'Drawing - ' + row[2], {'cleared':date}, [
					('Assets.NCA.CurAss.Cash.Current', - row[3]),
					('Assets.NCA.CurLia.Drawings', row[3])
					])
			output.append(tran)
		return output
	
	def doSales(self):
		output = []
		for row in self.sales:
			id = row[0]
			date = roundtime(row[1].value)
			customer = row[2]
			consult = row[5]   # sales category 1 - actual income
			exppassed = row[6]   # sales category 2 - expense charges		
			vat = row[7]
			gross = row[8]
			err = gross - (consult + exppassed + vat)
			if abs(err) >= 0.01:
				print 'Error %0.2f with %d'% (err, id)
			

			# sale transaction
			
			saletran = (date, 'Sale: ' + customer, 
						{'Customer':customer,
						'SaleID':id	},
						[
						('Capital.PL.Sales.Consulting',- consult),
						('Capital.PL.Sales.ExpPassed',- exppassed),
						('Assets.NCA.CurLia.VAT.OnSales',- vat),
						('Assets.NCA.CurAss.Debtors',gross),
						])
			output.append(saletran)
			
			# payment transaction
			if row[10] <> None:
				datepaid = roundtime(row[10].value)
				payment_tran = (datepaid, 'Payment Received: ' + customer,
							{
								'Customer':customer,
								'SaleID':id,
								'cleared': datepaid
							},
							[
								('Assets.NCA.CurAss.Debtors',-gross),
								('Assets.NCA.CurAss.Cash.Current',gross)
							])
				output.append(payment_tran)
					
		return output
						
		
	
	def doExpenses(self):
		expenses = []
		for d in self.expenses:
			# either one or two expenses depending on payment method
			if d['paidfrom'] == 'Cash':
				tran = (roundtime(d['date'].value),'Expense: ' + d['what'], 
						{'expenseid':d['expenseid'],
						'who':d['who'],
						'paidfrom':d['paidfrom']},
						[
							('Capital.PL.Expenses.'+d['category'], d['netamount']),
							('Assets.NCA.CurLia.VAT.OnPurchases', d['vatamount']),
							('Assets.NCA.CurLia.OwnersExpenses', - d['grossamount'])
						]
					)
				if abs(balance(tran)) >= 0.01:
					display(tran)
					raise AccountsError, 'Unbalanced Transaction'
				expenses.append(tran)
			elif d['paidfrom'] == 'DD':
				tran = (roundtime(d['date'].value),'Expense: ' + d['what'], 
						{'expenseid':d['expenseid'],
						'who':d['who'],
						'paidfrom':d['paidfrom'],
						'cleared':roundtime(d['cleared'].value)},
						[
							('Capital.PL.Expenses.'+d['category'], d['netamount']),
							('Assets.NCA.CurLia.VAT.OnPurchases', d['vatamount']),
							('Assets.NCA.CurAss.Cash.Current', - d['grossamount'])
						]
					)
				if abs(balance(tran)) >= 0.01:
					display(tran)
					raise AccountsError, 'Unbalanced Transaction'
				expenses.append(tran)
			elif d['paidfrom'] == 'MC':
				tran = (roundtime(d['date'].value),'Expense: ' + d['what'], 
						{'expenseid':d['expenseid'],
						'who':d['who'],
						'paidfrom':d['paidfrom'],
						'cleared':roundtime(d['cleared'].value)},
						[
							('Capital.PL.Expenses.'+d['category'], d['netamount']),
							('Assets.NCA.CurLia.VAT.OnPurchases', d['vatamount']),
							('Assets.NCA.CurLia.CreditCard', - d['grossamount'])
						]
					)
				if abs(balance(tran)) >= 0.01:
					display(tran)
					raise AccountsError, 'Unbalanced Transaction'
				expenses.append(tran)
			elif d['paidfrom'] == 'Cheque':   #both a bil and a payment
				# first the bill
				billtran = (roundtime(d['date'].value),'Expense: ' + d['what'], 
						{'expenseid':d['expenseid'],
						'who':d['who'],
						'paidfrom':d['paidfrom'],
						'cleared':roundtime(d['cleared'].value)},
						[
							('Capital.PL.Expenses.'+d['category'], d['netamount']),
							('Assets.NCA.CurLia.VAT.OnPurchases', d['vatamount']),
							('Assets.NCA.CurLia.Creditors', - d['grossamount'])
						]
					)
				if abs(balance(billtran)) >= 0.01:
					display(billtran)
					raise AccountsError, 'Unbalanced Transaction'
				expenses.append(billtran)
			
				# payment later
				if d['cleared'] <> None:
					dict = {'expenseid':d['expenseid'],
						'who':d['who'],
						'paidfrom':d['paidfrom'],
						'chequeno':d['chequeno'],
						'cleared':roundtime(d['cleared'].value)
						}
					paytran = (roundtime(d['cleared'].value),'Pay Bill: ' + d['what'], 
						dict,
						[('Assets.NCA.CurLia.Creditors', d['grossamount']),
						('Assets.NCA.CurAss.Cash.Current', - d['grossamount'])
						]
						)
					if abs(balance(paytran)) >= 0.01:
						display(paytran)
						raise AccountsError, 'Unbalanced Transaction'
					expenses.append(paytran)
			else:  # unknown payment type
				pprint(d)
				raise AccountsError, 'Unknown payment type for expense %d' % d['expenseid']


		return expenses
						

def getDatePaid(aTran):
	try:
		datepaid = aTran[2]['cleared']
	except:
		datepaid = ymd2time(2000,1,1)    #well after our period
	return datepaid

def getClearedReport(aBookset, anAccount):
	lines = []
	
	for tran in aBookset.journal:
		for line in tran[3]:
			(acct, amount) = line[0:2]
			if acct == anAccount:
				bits = [
					getDatePaid(tran), #date paid
					tran[0],  #date
					tran[1],  #comment
					amount]
				lines.append(bits)
	lines.sort()    # does it on date paid
	total = 0
	for line in lines:
		total = total + line[3]
		line.append(total)
	return lines

	
def getBookSet():
	# return it
			
					
	# first load opening balances
	B = BookSet()
	B.loadFromText(WORKDIR + 'opening9798.log')
	B.journal[0][2]['cleared'] = ymd2time(1997,3,31)
	
	raw = RawData()
	raw.fetch()
		
	# add drawings
	drawings = raw.doDrawings()
	B.journal = B.journal + drawings
	

	# add sales and payments
	sales = raw.doSales()
	B.journal = B.journal + sales
		
	# adjustments to sales:	
	#1. write off AppBio
	writeoff = (ymd2time(1998,3,31),
			'AppBio Bad Debt write-off',
			{'SaleID':9710002, 'Customer':'Applied Biometrics'},
			[('Capital.PL.Sales.Consulting',4275.86),
			('Capital.PL.Sales.ExpPassed',198.62),
			('Capital.PL.BadDebtProvision',-4474.48)]
			)
	B.journal.append(writeoff)

	# expenses
	B.journal = B.journal + raw.doExpenses()
	# some of them are assets...
	mapping = {
		'Capital.PL.Expenses.ComputerEquipment':'Assets.Fixed.Computer.OriginalCost',
		'Capital.PL.Expenses.OfficeEquipment':'Assets.Fixed.Office.OriginalCost',

		}
	print 'Remapping expenses'
	#B.listAccount('Capital.PL.Expenses.ComputerEquipment')
	B.map(mapping)
	
	# add in the only payment from last year
	B.journal.append((ymd2time(1997,4,11), 
			'Payment (last year): Principia', 
			{'DateCleared':ymd2time(1997,4,11)},
			[
				('Assets.NCA.CurAss.Debtors', -3888),
				('Assets.NCA.CurAss.Cash.Current', 3888)
			]
			))
				

	# other things only appearing on bank statements
	Pension = [  
		((1997,4,2), 263.15),
		((1997,4,29), 263.15),
		((1997,5,29), 263.15),
		((1997,7,1), 263.15),
		((1997,7,29), 263.15),
		((1997,8,29), 263.15),
		((1997,9,30), 263.15),
		((1997,10,29), 263.15),
		((1997,12,1), 276.30),
		((1997,12,30), 276.30),
		((1998,1,29), 276.30),
		((1998,3, 3), 276.30),
		((1998,3,31), 276.30)
		]
	for ((y,m,d), amount) in Pension:
		t = ymd2time(y,m,d)
		tran = (t,'Pension',{'cleared':t},[
			('Capital.PL.Expenses.Pension',amount),
			('Assets.NCA.CurAss.Cash.Current', -amount)])
		B.journal.append(tran)

	ContractorsInsuranceDates = [
		((1997,4,1), 26.32),
		((1997,4,30), 26.32),
		((1997,5,30), 26.32),
		((1997,7,2), 26.32),
		((1997,7,30), 26.32),
		((1997,8,29), 26.32),
		((1997,10,1), 26.32),
		((1997,10,29), 26.32),
		((1997,11,28), 26.32),
		((1997,12,31), 26.32),
		((1998,1,30), 27.23),
		((1998,3,4), 27.23)
		]
		
		
		
	for date_tuple, amount in ContractorsInsuranceDates:
		t = ymd2time(date_tuple[0],date_tuple[1],date_tuple[2])
		tran = (t,'PIC Insurance',{'cleared':t},[
			('Capital.PL.Expenses.ContractorsInsurance',amount),
			('Assets.NCA.CurAss.Cash.Current', -amount)])
		B.journal.append(tran)

	LifeInsuranceDates = [
			(1997,4,7),
			(1997,5,6),
			(1997,6,6),
			(1997,7,7),
			(1997,8,6),
			(1997,9,8),
			(1997,10,6),
			(1997,11,6),
			(1997,12,8),
			(1998,1,8),
			(1998,2,6),
			(1998,3,6)			
		]
	for date_tuple in LifeInsuranceDates:
		t = ymd2time(date_tuple[0],date_tuple[1],date_tuple[2])
		tran = (t,'Life Insurance',{'cleared':t},[
			('Capital.PL.Expenses.ContractorsInsurance',10.0),
			('Assets.NCA.CurAss.Cash.Current', -10.0)])
		B.journal.append(tran)


	BusinessCardPayments = [
		((1997,4,10),	457.67),
		((1997,5,12),	74.33),
		((1997,6,11),	716.96),
		((1997,7,11),     309.73),
		((1997,8,12),      6.05),
		((1997,9,10),      588.04),
		((1997,10,13),     1604.66),
		((1997,11,12),     597.53),
		((1997,12,10),	1334.18),
		((1998,1,13),      308.85),
		((1998,2,11),	 888.08),
		((1998,3,11),      354.52)
		]
		
	for ((y,m,d),x) in BusinessCardPayments:
		tran = (ymd2time(y,m,d),'Business Card Payment',{'cleared':ymd2time(y,m,d)},[
				('Assets.NCA.CurAss.Cash.Current',-x),
				('Assets.NCA.CurLia.CreditCard',x)])
		B.journal.append(tran)


	BusDevLoan = [  #date, principal, interest
			((1997,4,14),     72.72,	25.04),
			((1997,4,16),   1284.14,       0.00),
			((1997,5,13),	73.49,      11.99),
			((1997,6,13),     31.13,       9.84),
			((1997,7,14),     31.46,	 9.51),
			((1997,8,13),     31.79,	 9.18),
			((1997,9,14),     32.13,	 8.84),
			((1997,10,14),    32.47,	 8.50),
			((1997,11,13),    32.82,	 8.15),
			((1997,12,14),    33.16,	 7.81),
			((1998,1,14),     33.52,	 7.45),
			((1998,2,13),     33.87,	 7.10),
			((1998,3,14),     34.23,	 6.74),
		]
	for ((y,m,d),prin,int) in BusDevLoan:
		date = ymd2time(y,m,d)
		tran = (date, 'Bus Dev Loan Payment', {'cleared':date},[
				('Assets.NCA.CurAss.Cash.Current',- prin - int),
				('Assets.LongTermLiabilities.BankLoan',prin),
				('Capital.PL.Expenses.Interest',int)])
		B.journal.append(tran)
		
	# inter-bank movements
	B.journal.append((ymd2time(1997,5,19),'from Business Reserve',{'cleared':ymd2time(1997,5,19)},[
					('Assets.NCA.CurAss.Cash.Current',2000),
					('Assets.NCA.CurAss.Cash.Reserve',-2000)])
					)
	B.journal.append((ymd2time(1997,6,20),'from Business Reserve',{'cleared':ymd2time(1997,6,20)},[
					('Assets.NCA.CurAss.Cash.Current',4000),
					('Assets.NCA.CurAss.Cash.Reserve',-4000)])
					)

	B.journal.append((ymd2time(1997,9,15),'from Petty Cash',{'cleared':ymd2time(1997,9,15)},[
					('Assets.NCA.CurAss.Cash.Current',76.75),
					('Assets.NCA.CurAss.Cash.Reserve',-76.75)])
					)


	# Bank Charges
	BankCharges = [
		((1997,11,28), 4.90),
		((1997,12,31), 5.30),
		((1998,1,30),  9.85),
		((1998,2,27),  6.91),
		((1998,3,31),  5.17)
		
		]
	for ((y,m,d),amount) in BankCharges:
		date = ymd2time(y,m,d)
		tran = (date,'Bank Charges',{'cleared':date},[
					('Assets.NCA.CurAss.Cash.Current',-amount),
					('Capital.PL.Expenses.BankCharges',amount)
					]
					)
		B.journal.append(tran)
		
	

	
	# PAYE
	PAYEpayments = [
		((1997,5,19),(1997,5,22),996),
		((1997,5,19),(1997,5,22),996),
		((1997,12,5),(1997,12,10), 1922.43)
		]
	for (paid, cleared, amount) in PAYEpayments:
		datepaid = ymd2time(paid[0],paid[1],paid[2])
		datecleared = ymd2time(cleared[0],cleared[1],cleared[2])
		
		tran = (datepaid, 'Pay PAYE/NI', {'cleared':datecleared},[
				('Assets.NCA.CurAss.Cash.Current',- amount),
				('Assets.NCA.CurLia.PAYE', amount)
				])
		B.journal.append(tran)
	
	
	
	# corp tax from last year
	datepaid = ymd2time(1997,6,20)
	datecleared = ymd2time(1997,7,4)
	amount = 4153.75
	tran = (datepaid, 'Pay ACT due', {'cleared':datecleared},[
				('Assets.NCA.CurAss.Cash.Current',- amount),
				('Assets.NCA.CurLia.CorpTax', amount)
				])
	B.journal.append(tran)
	

	# error adjustments
	
	# made out a cheque to someone for XXX.87 instead of XXXX.78 - tidy the 9p 
	B.journal.append(
		(ymd2time(1997,6,2),'Cheque error correction',{'cleared':ymd2time(1997,6,2)},[
				('Assets.NCA.CurAss.Cash.Current',-0.09),
				('Assets.NCA.CurLia.OwnersExpenses',0.09)]
				)
			)

	# HPS repaid a cheque I thought I had forgotten a year earlier
	B.journal.append(
		(ymd2time(1998,3,10), 'HPS repaid last year',{'cleared':ymd2time(1998,3,10)},[
				('Assets.NCA.CurAss.Cash.Current',430.80),
				('Capital.PL.Sales.ExpPassed',-430.80)]))
	
	# Initial credit card balance was 457.67, not 264.30.  Fix this on 1st April
	B.journal.append(
		(ymd2time(1997,4,1), 'Credit Card opening balance error',{'cleared':ymd2time(1997,4,1)},[
				('Assets.NCA.CurLia.CreditCard',-193.37), 
				('Assets.NCA.CurLia.OwnersExpenses',193.37)])
			)
								
	# withdrew £1000 personal on credit card to pay Alisa's fees by phone
	B.journal.append(
		(ymd2time(1997,11,21), 'Drawings',{'cleared':ymd2time(1997,11,24)},[
				('Assets.NCA.CurLia.CreditCard',-1000.00), 
				('Assets.NCA.CurLia.Drawings',1000.00)])
			)
	
	# withdrew £80 to petty cash on business in Sweden
	B.journal.append(
		(ymd2time(1998,3,24), 'Cash Withdraw',{'cleared':ymd2time(1998,3,26)},[
				('Assets.NCA.CurLia.CreditCard',-80.33), 
				('Assets.NCA.CurLia.OwnersExpenses',80.33)])
			)
	
	
	
	# year end PAYE
	YEAREND = ymd2time(1998,3,31)
	#	Contributing elements			
	#		Salary	18500	
	#				
	#	a	Net Salary	13707.42	
	#	b	PAYE	3200.5	
	#	c	NIC	1592.08	
	#	d	Total Salary	18500	
	#				
	#	e	Employers' NIC	1850	
	#	f	Gross cost	20350	
	#				
	#	g	IR payment	6642.58	

	B.journal.append((YEAREND,'Payroll - salary & ni',{},[
			('Capital.PL.Expenses.Wages', 20350),
			('Assets.NCA.CurLia.PAYE', -6642.58),
			('Assets.NCA.CurLia.Drawings', -13707.42)
			]))
	
	B.journal.append((YEAREND,'Dividend',{},[
			('Assets.NCA.CurLia.Drawings', -14664.35),
			('Assets.NCA.CurLia.CorpTax', -2932.87),
			('Capital.Dividend199798', 17597.22)
			]))
	
	
	# Expense claim settlement
	B.journal.append(
		(ymd2time(1998,3,31), 'Expense claim for year', {}, [
				('Assets.NCA.CurLia.OwnersExpenses',4218.55),
				('Assets.NCA.CurLia.Drawings', -4218.55)])
			)

	
	# year end depreciation
	B.journal.append(
		(ymd2time(1998,3,31), 'Depreciation for year', {}, [
				('Assets.Fixed.Computer.Depreciation',-2538.88),
				('Assets.Fixed.Office.Depreciation', -48.25),
				('Capital.PL.Expenses.Depreciation', 2587.13)])
			)

			
	B.compact()   # remove empty lines
	B.journal.sort()		
	if abs(B.checksum()) >= 0.01:
		raise AccountsError, 'Bookset Checksum error'

	return B

def current(start=(1997,1,1)):

	startdate = ymd2time(start[0],start[1],start[2])
	
	B = getBookSet()
	rpt = getClearedReport(B,'Assets.NCA.CurAss.Cash.Current')
	
	
	textfilename = WORKDIR + 'current.txt'
	f = open(textfilename,'w')
	for row in rpt:
		if row[1] >= startdate:	
			f.write('%s  %s  %-30s   %10.2f   %10.2f\n' % (ddmmyyyy(row[0]),ddmmyyyy(row[1]),row[2],row[3],row[4]))
	f.close()
	os.system('start ' + textfilename)
	
def credit(start=(1997,1,1)):

	startdate = ymd2time(start[0],start[1],start[2])
	
	B = getBookSet()
	rpt = getClearedReport(B,'Assets.NCA.CurLia.CreditCard')
	
	
	textfilename = WORKDIR + 'credit.txt'
	f = open(textfilename,'w')
	for row in rpt:
		if row[1] >= startdate:	
			f.write('%s  %s  %-30s   %10.2f   %10.2f\n' % (ddmmyyyy(row[0]),ddmmyyyy(row[1]),row[2],row[3],row[4]))
	f.close()
	os.system('start ' + textfilename)

	
def run():
	B = getBookSet()
	B.saveAsText(WORKDIR + 'robanal9798.log')
	
	#make a list of accounts too:
	f = open(WORKDIR + 'accounts_used.txt','w')
	for acct in B.acctList():
		f.write(acct + '\n')
	f.close()
	
	print 'Saved.'

# utility to do year ends and print to console
def combine(year1, year2):
    master = {}
    for (acct, amt) in year1:
        master[acct] = [amt,0]
    for (acct, amt) in year2:
        if master.has_key(acct):
            master[acct][1] = amt
        else:
            master[acct] = [0, amt]


    table = master.items()
    table.sort()
    for row in table:
        print row[0],'\t',row[1][0],'\t',row[1][1]
    return table

def printtb():
    end97 = mktime((1997,3,31,0,0,0,0,0,0))
    end98 = mktime((1998,3,31,0,0,0,0,0,0))
    B = getBookSet()
    year1 = B.BalanceOn(end97)
    year2 = B.BalanceOn(end98)
    combine(year1, year2)
        

if __name__ == '__main__':
	run()