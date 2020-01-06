## dates module
"""
asc2sec parses formats like: 
	dd/m/yy
	dd/mm/yyyy
	dd/mm/yy hh:mm:ss

and returns time in seconds - rounded to nearest for time being.

sec2asc gives dd/mm/yyyy format, and adds time if not zero.
the test functions at the end seem to work out OK.

Should be expanded to read all formats, but with an optimised check
for the standard one first.

For a real application I would take a hard look at mxDateTime which
does more sophisticated parsing and supports a full range of dates.


"""

from time import *
import string

dateseparator = '/'	#e.g. 27/03/96 or 27/03/1996
timeseparator = ':'            	#e.g. 17:53:07
centuryguesspoint = 50	#if 27/01/49, assume 2049; if 27/01/51, assume 1951
#hack added to make the date format 23-Jan-97 for the book
defaultformat = 'DD-MMM-YYYY'

#some constants to use later.  Coincidentally, these are indexes into
#the time tuple, except for WEEKS which will cause an error if called
YEARS	=	0
MONTHS=		1
DAYS	=	2
HOURS	=	3
MINUTES = 	4
SECONDS = 	5
WEEKS	=	10


ONE_SECOND = 1.0/86400.0

# handy list of years ends from 1995
YEARENDS = [820368000.0, 851990400.0, 883526400.0, 915062400.0, 946598400.0, 978220800.0, 1009756800.0]

SHORT_MONTHS = string.split('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec')
YEARLENGTH = 365 * 24 * 60 * 60.0  # note floating point


# these two constants should be well before or after anything in your system
EARLY = 0
LATE = mktime((2038,1,15,0,0,0,0,0,0))   #nearly the last day in Unix time system

def sec2asc(aSecs):
	tup = gmtime(int(aSecs))
	if defaultformat == 'DD-MMM-YYYY':
		month = SHORT_MONTHS[tup[1]-1]
		date = '%d-%s-%d' % (tup[2],month,tup[0])
	else:
		date = '%d/%d/%d' % tuple(tup[0:2])
	if tup[3:6]==(0,0,0):
		return date
	else:
		strtime = '%d:%2d:%2d' % tuple(tup[3:6])
		return date + ' ' + strtime

def asc2sec(txt):
	bits = string.split(txt)  #up to two bits
	if len(bits)==1:
		return int(parseDate(bits[0]))
	elif len(bits)==2:
		return int(parseDate(bits[0])+parseTime(bits[1]))
	elif len(bits)>2:
		return 0



def parseDate(txt):
	"""parses a string like either dd/mm/yy or 
	dd-mmm-yy (hacked at publishers insistence)
	and returns seconds"""
	if string.find(txt, '-') >= 0:
		return parseMMMDate(txt)
		
	bits = string.splitfields(txt,dateseparator)
	bits = map(string.atoi,bits)  #convert to numbers
	if len(bits)<>3:
		return 0
	yy = bits[2]
	if yy < 100:
		if yy < centuryguesspoint:
			yy = yy + 2000
		else:
			yy = yy + 1900
	
	mm = bits[1]
	dd = bits[0]
	
	tup = (yy,mm,dd,0,0,0,0,0,0)
	return mktime(tup)

def parseMMMDate(text):
	bits = string.splitfields(text, '-')
	if len(bits) <> 3:
		return 0
	dd = string.atoi(bits[0])
	yy = string.atoi(bits[2])
	if yy < 100:
		if yy < centuryguesspoint:
			yy = yy + 2000
		else:
			yy = yy + 1900
	mm = SHORT_MONTHS.index(string.capitalize(bits[1])) + 1
	if mm == 0:
		return 0
	return mktime((yy,mm,dd,0,0,0,0,0,0))
	

def parseTime(txt):  
	"assumes hh:mm:ss or hh:mm"
	bits = map(string.atoi,string.splitfields(txt,timeseparator))
	if len(bits)<>3:
		return 0
	hh=bits[0]
	nn=bits[1]
	ss=bits[2]
	return ss + (60 * nn) + (3600 * hh)

def now():
	return time()

def testnow():
	"runs the obvious identity test on the current time"
	secs = time()
	print 'time in seconds: ',secs
	
	asc = sec2asc(secs)
	print 'time in ascii:   ',asc

	secs2 = asc2sec(asc)
	print 'time #2 in seconds: ',secs2
	
	if int(secs) == int(secs2):
		print 'passed'
		return 1
	else:
		print 'failed'
		return 0

def testasc(txt):
	return sec2asc(asc2sec(txt))

#
#	date manipulation functions
#

def later(secs,quantity,units=DAYS):
	if units == SECONDS:
		return secs + quantity
	elif units == MINUTES:
		return secs + (quantity * 60)
	elif units == HOURS:
		return secs + (quantity * 3600)
	elif units == DAYS:
		return secs + (quantity * 86400)
	elif units == WEEKS:
		return secs + (quantity * 7 * 86400)
	elif units == MONTHS:
		"""
		returns a time n months later.  If we end up on 29 feb and
		it doesn't exist, skips FORWARD a day.  Needs tidying up.
		"""
		(yy,mm,dd,hh,nn,ss,spam,eggs,cabbage) = gmtime(secs)  #don't need last three
		mm = mm + quantity
		while mm > 12:   #have we gone a year forward?
			mm = mm - 12
			yy = yy + 1
		return mktime((yy,mm,dd,hh,nn,ss,spam,eggs,cabbage))
	elif units == YEARS:
		(yy,mm,dd,hh,nn,ss,spam,eggs,cabbage) = gmtime(secs)  #don't need last three
		yy = yy + quantity
		return mktime((yy,mm,dd,hh,nn,ss,spam,eggs,cabbage))
	else:
		print "Later function doesn't understand units of",units
		return secs

		
def LastDayOfMonth(secs):
	#first get the month
	secs = int(ONE_SECOND * secs) * 86400
	mm = gmtime(secs)[1]
	while gmtime(secs)[1] == mm:
		secs = secs + 86400  #add a day until next month
	#then backtrack one
	secs = secs - 86400
	return secs

def LastSecondOfMonth(secs):
	#first get the month
	secs = int(ONE_SECOND * secs) * 86400
	mm = gmtime(secs)[1]
	while gmtime(secs)[1] == mm:
		secs = secs + 86400  #add a day until next month
	#then backtrack one second	
	secs = secs - 1
	return secs

def FirstDayOfMonth(secs):
	(yy,mm,dd,hh,nn,ss,spam,eggs,cabbage) = gmtime(secs)  #don't need last three
	return mktime((yy,mm,1,0,0,0,0,0,0))


def MonthStartsCovering(date1, date2):
	theDate = FirstDayOfMonth(date1)
	latest = LastDayOfMonth(date2)
	result = [theDate]
	while theDate <= latest:
		theDate = later(theDate, 1, MONTHS)
		result.append(theDate)
	return result
		

def MonthEndsCovering(date1, date2):
	#with (say) 17th dec 95 to 1st april 2002, gives 31/12/95, 31/01/96...30/4/2002
	return map(lambda x: x - 86400, MonthStartsCovering(date1, date2))[1:]

def FirstDayOfYear(secs):
	(yy,mm,dd,hh,nn,ss,spam,eggs,cabbage) = gmtime(secs)  #don't need last three
	return mktime((yy,01,01,0,0,0,0,0,0))

	
def LastDayOfYear(secs):
	(yy,mm,dd,hh,nn,ss,spam,eggs,cabbage) = gmtime(secs)  #don't need last three
	return mktime((yy,12,31,0,0,0,0,0,0))

def YearEndsCovering(date1, date2):
	#cheat
	return YEARENDS
		
def yyyymm(secs):
	# a useful index for data analysis
	(yy,mm,dd,hh,nn,ss,spam,eggs,cabbage) = gmtime(secs)  #don't need last three
	return yy * 100 + mm

def ddmmmyyyy(secs):
	(yy,mm,dd,hh,nn,ss,spam,eggs,cabbage) = gmtime(secs)  #don't need last three
	monthname = SHORT_MONTHS[mm]
	return '%d-%s-%d' % (dd, monthname, yy)
    	
##test stuff
																
def testlater(asc,qty,units):
	return sec2asc(later(asc2sec(asc),qty,units))

def testlater2(start=time(),qty=7):
	startasc = sec2asc(start)
	print 'start date:',startasc
		
	for i in range(11):
		print i,'   ',
		print testlater(startasc,qty,i)

