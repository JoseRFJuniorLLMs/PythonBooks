# creates a set of imaginary data
# for a small computer consulting firm

# this is a "Business Model"

from stdaccts import *
from dates import *
from bookset import *


# top down approach - returns a bookset
def run():
	"returns a BookSet"
	BS = BookSet()

def Invest(bs):
	# first the financing
	tran = MakeTransfer(asc2sec('3/1/98'),
		'Initial Investment',
		Match('Cash'), 
		Match('ShareCap'),
		10000)
	bs.add(tran)


# assume we borrow 20000 at 1% per month - unsecured small business rates
# over 5 years, repayments starting instantly
balance = 20000
rate = 0.01
drawdate = asc2sec('1/2/98')
periods = 60
payment = 444.8890   # I cheated and used Excel
cashacct = Match('Cash')
loanacct = Match('Loans')
interestacct = Match('InterestPaid')
date = drawdate
# now draw the money
tran = MakeTransfer(
		drawdate, 
		'Borrow money from bank',
		cashacct,
		loanacct,
		20000)

# now the repayments
for i in range(periods):
	date = later(date, 1, MONTHS)
	interest = balance * rate
	balance = balance + interest - payment
	tran = (date,'Loan Repayment %d of 60' % (i+1), {},
			[
			(cashacct, 0 - payment),
			(interestacct, interest),
			(loanacct, payment - interest)
			]
		)
	









