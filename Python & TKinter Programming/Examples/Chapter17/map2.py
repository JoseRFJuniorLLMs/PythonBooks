from string import maketrans, translate

def Y2K(instr):
	return translate(instr, maketrans('yY', 'kK'))

list = ['thirty', 'Year 2000', 'century', 'yellow']

print map(None, list, map(Y2K, list))

