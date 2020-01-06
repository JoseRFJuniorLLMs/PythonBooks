# financial functions - crude protoypes
# part of the doubletalk toolkit
# copyright andy robinson 1998

"""
Financial Functions - NPV and IRR - for a stream
of unevenly spaced cash flows
"""

# python uses seconds for now, define a year as 365 days.  Sod leap years,
# I don't care at this stage




from doubletalk.dates import *

def PresentValue(TimeNow, FutureTime, FutureValue, YearlyRate):
	years = (FutureTime - TimeNow) / YEARLENGTH
	rate = ((1+YearlyRate) ** years) - 1
	discountfactor = 1/(1+rate)
	return FutureValue * discountfactor

PV = PresentValue    #shorter alias

def NetPresentValue(TimeNow, YearlyRate, CashFlows):
	"Values a series of cash flows expressed as (date, amount) pairs"
	npv = 0
	for flow in CashFlows:
		(date, amount) = flow	#unpack it
		npv = npv + PresentValue(TimeNow, date, amount, YearlyRate)
	return npv

NPV = NetPresentValue

def InternalRateOfReturn(CashFlows, guess=0.1):
	"""Work out the internal rate of return of a series
	of cash flows. i.e. the discount rate giving an NPV 
	of zero."""
	
	maxtries = 100
	accuracy = 1e-10
	tries = 0
	#pick any date to use - take the first
	valdate = CashFlows[0][0]

	# arbitrart different guess to start loop
	last_guess = guess + 1	
	
	while abs(last_guess - guess) > accuracy:
		last_guess = guess
		x0 = guess
		if guess == 0:
			x1 = 0.1
		else:
			x1 = guess * 1.1
		y0 = NPV(valdate, x0, CashFlows)
		y1 = NPV(valdate, x1, CashFlows)
		slope = (y1-y0)/(x1-x0)
		guess = x0 - (y0/slope)
				
		print 'try: %d, rate: %f, NPV: %0f' % (tries, x0, y0)
		tries = tries + 1
		if tries > maxtries:
			raise ValueError, 'No solution found to IRR'

	return guess
	
		
IRR = InternalRateOfReturn
		

def BetterGuess(func, guess):
	# try to find a better approximation to zero of a function
	
	x0 = guess
	if guess == 0:
		x1 = 1
	else:
		x1 = guess * 1.1

	y0 = func(x0)
	y1 = func(x1)
	slope = (y1-y0)/(x1-x0)
	return x0 - (y0/slope)

def NRSolve(func, guess = 0):
	# try to find zero of a function
	maxtries = 20
	accuracy = 1e-10
	lastguess = guess + 1
	while abs(guess - lastguess) > accuracy:
		lastguess = guess
		guess = BetterGuess(func, guess)
		maxtries = maxtries - 1
		if maxtries == 0:
			raise ValueError, "No solution found"
	return guess



#some sample data

def test():
	#ready-made dates from our dates module
	e95, e96, e97, e98, e99, e2000 = YEARENDS[0:6]  
	
	bond1 = [
		(e95, -100),
		(e96, 10),
		(e97, 10),
		(e98, 10),
		(e99, 10),
		(e2000, 10), (e2000,100)
		]
	rate = 0.10
	npv = NetPresentValue(e95, rate, bond1) 
	print "Value of bond at end 95 at %0.2f = %0.1f" % (rate, npv)
	print "IRR of bond is %f" % (IRR(bond1))
	print
	
	# do a capital business
	gym = [
		(e95, -50000), #seed capital
		(e96, -250000), #construction
		]
	
	year = e97
	profit = 20000

	#steadily growing income for 10 years
	for i in range(10):  		
		gym.append((year, profit))
		profit = profit * 1.2
		year = year + YEARLENGTH
	
	#sell for six times earnings
	gym.append(year, profit * 6)

	#for flow in gym: 
	#	(date, amount) = flow
	#	print sec2asc(date), amount
		
	npv = NetPresentValue(e98, rate, gym)
	print 'gym project is worth %0.0f at rate %f' % (npv, rate)
	irr = InternalRateOfReturn(gym)
	print 'IRR of gym project is %0.4f' % (irr)
		

if __name__ == '__main__':
	test()











