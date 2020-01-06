# standard chart of accounts
# suitable for simple management accounts in a tax-free world
#
# also function for flipping between a tab-indented form
# and 'ancestry lists'.  Does not test for crazy hierarchies.
#
# also some functions for building transactions easily

import string

stdtree = """
Assets
	Fixed
	NCA
		CurrAss
			Cash
			TradeDebtors
		CurrLia
			TradeCreditors
	LongTermLia
		Loans
Capital
	ShareCapital
	PL
		GrossProfit
			Sales
			CostOfSales
		Overheads
"""





def GetIndent(txt):
	"returns number of leading tabs"
	indent = 0
	while txt[indent] == '\t':
		indent = indent + 1
	return indent

def TextTreeToAccountsList(tree):
	"Splits up a tab-indented text tree into a list of accounts"
	lines1 = string.split(tree, '\n')
	
	# strip any null lines or comment lines
	lines2 = []
	for line in lines1:
		stripped = string.strip(line)
		if stripped == '':
			continue
		if stripped[0] =='#':
			continue
		lines2.append(line)
	
	ancestry = []  	# keep a stack of accounts
	accts = []		# put results here
	for line in lines2:
		level = GetIndent(line)
		acct = string.strip(line)
		if level > len(ancestry):
			ancestry.append(acct)
		else:
			ancestry = ancestry[0:level] + [acct]
		accts.append(string.join(ancestry,'.'))
	return accts
	
def AccountsListAsTextTree(list):
	"takes an accounts list and returns list of indented strings"
	results = []
	for line in list:
		ancestry = string.split(line, '.')
		tabs = len(ancestry) - 1
		str = '\t' * tabs + ancestry[-1]
		results.append(str)
	return results


stdlist = TextTreeToAccountsList(stdtree) 

def Match(abbrev):
	"finds a matching account - first string match"
	global stdlist
	for acct in stdlist:
		if string.find(string.upper(acct), string.upper(abbrev)) <> -1:
			return acct
	#not found - return something obvious
	return '<unmatched "' + abbrev + '">'




#
#
#     functions to help construct transactions in this chart of accounts
#
#

def MakeTransfer(date, comment, acct1, acct2, amount):
	global stdlist
	return (
		date,
		comment,
		{},
		[
			(Match(acct1), amount),
			(match(acct2), 0 - amount)
		]
		)


def test():
	print 'Testing tree parser'
	list = TextTreeToAccountsList(stdtree)
	for acct in list:
		print acct
	print 'OK'