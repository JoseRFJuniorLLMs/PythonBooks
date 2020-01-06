# test script to list out all transactions
# whose comments begin with a capital 'B'

for tran in TheBookSet:
	if tran.comment[0] == 'B':
		tran.display()

print 'done'