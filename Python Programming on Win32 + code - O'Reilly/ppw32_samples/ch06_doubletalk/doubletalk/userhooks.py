# userbookset.py
"""
UserBookSet - provides mechanisms for notification and custom views
written by users
"""

from doubletalk.bookset import BookSet
from doubletalk.transac import Transaction
import doubletalk.datastruct
import time  # used by a sample view

class Validator:
    """A delegate which is informed before changes occur,
    and which may veto them. Should provide a description
    Calling UserBookSet.addDelegate links it together
    with the BookSet.  Users subclass this to get new
    behaviour"""
    
    def setBookSet(self, aBookSet):
        self.BookSet = aBookSet
    
    def getDescription(self):
        return 'abstract base class for Validators'
        
    # hooks for validation before the event
    def mayAdd(self, aTransaction):
        return 1  # zero aborts the operation
    def mayEdit(self, index, newTransaction):
        return 1
    def mayRemove(self, index):
        return 1
    def mayRenameAccount(self, oldname, newname):
        return 1

    
    
class View:
    """This delegate is informed of all changes after they occur,
    and returns a 2d array of data when asked."""
    def setBookSet(self, aBookSet):
        self.BookSet = aBookSet
        self.recalc()

    def getDescription(self):
        return 'abstract base class for Views'
    
    # hooks for notification after the event
    def didAdd(self, aTransaction):
        pass
    def didEdit(self, index, newTransaction):
        pass
    def didRemove(self, index):
        pass
    def didRenameAccount(self, oldname, newname):
        pass
    def didChangeDrastically(self):
        #can be used to notify of major changes such as file/open
        self.recalc()
                
    def recalc(self):
        #override this to work out the data
        pass
    
    def getData(self):
        return [()]  # simple 2-d array for display

class UserBookSet(BookSet):
    def __init__(self):
        BookSet.__init__(self)
        self.validators = []
        self.validator_lookup = {}
        self.views = []
        self.view_lookup = {}

    def listDelegates(self):
        # utility to tell us what's up
        print 'Validators - may approve edits:'
        print '------------------------------'
        for v in self.validators:
            print repr(v), ':', v.getDescription()
            
        print 
        print 'Views - informed of changes:'
        print '------------------------------'
        for v in self.views:
            print repr(v), ':', v.getDescription()

    
    def addValidator(self, aValidator, aName):
        # join them together
        self.validators.append(aValidator)
        self.validator_lookup[aName] = aValidator
        aValidator.setBookSet(self)
    
    def addView(self, aView, aName):
        # join them together
        self.views.append(aView)
        self.view_lookup[aName] = aView
        aView.setBookSet(self)
        
    def getViewData(self, aName):
        return self.view_lookup[aName].getData()
        
    def add(self, tran):
        for v in self.validators:
            if not v.mayAdd(tran):
                # rejected, stop
                return
                
        #call the inherited method
        BookSet.add(self, tran)
        
        # notify them all
        for v in self.views:
            v.didAdd(tran)
        
    def edit(self, index, newTran):
        for v in self.validators:
            if not v.mayEdit(index, newTran):
                return
        
        BookSet.edit(self, index, newTran)
        
        for v in self.views:
            v.didEdit(index, newTran)
        
    def remove(self, index):
        for v in self.validators:
            if not v.mayRemove(index):
                return
                
        #call the inherited method
        BookSet.remove(self, index)
        
        # notify them all
        for v in self.views:
            v.didRemove(index)
            
    def renameAccount(self, oldAcct, newAcct, compact=1):
        for v in self.validators:
            if not v.mayRenameAccount(oldAcct, newAcct):
                return
        
        BookSet.renameAccount(self, oldAcct, newAcct, compact=1)
        
        for v in self.views:
            v.didRenameAccount(self, oldAcct, newAcct)
            
class DateWindowValidator(Validator):
    """An example.  Prevents changes on or before a certain date
    locking the bookset"""

    def __init__(self, aDescription, aDate):
        Validator.__init__(self, aDescription)
        self.cutoff = aDate
    
    def mayAdd(self, aTransaction):
        return (aTransaction.date > self.cutoff)
    
    def mayEdit(self, index, newTransaction):
        oldtran = self.BookSet[index]
        if oldtran.date <= self.cutoff:
            return 0
        elif newTransaction.date <= self.cutoff:
            return 0
        else:
            return 1

    def mayRemove(self, index):
        tran = self.BookSet[index]
        return (tran.date > self.cutoff)
        
    # renameAccount will not break anything
    
def testValidator():
    
    from doubletalk.dates import *
    
    bs = UserBookSet()
    bs.load('demodata2.dtj')  #sample data from Jan - Mar 99
    
    bs[0].display()
    
    endJan99 = asc2sec('31/1/1999')
    datelock = DateWindowValidator('Date Cutoff at end January 1999', endJan99)
    bs.addValidator(datelock)
    
    tran = Transaction()
    tran.date = asc2sec('31/12/1998')
    tran.comment = 'this should not be allowed in'
    tran.addLine('MyCo.Capital.PL.Expense.Entertainment', 153.75)
    tran.addLastLine('MyCo.Assets.NCA.CurLia.ExpenseClaims')
    tran.validate()
    
    bs.add(tran)
    
    bs[0].display()  #should still be the same transaction
    


class MonthlyAccountActivity(View):
    """Keeps track of activity in an account.  Does
    smart recalculations."""
    
    def __init__(self, anAccount):
        self.account = anAccount
        self.balances = doubletalk.datastruct.NumDict()
    
    def getDescription(self):
        return 'Month end balances for ' + self.account
    
    def didAdd(self, tran):
        effect = tran.effectOn(self.account)
        if effect == 0:
            return
        else:
            #year and month as the key
            yymm = time.gmtime(tran.date)[0:2]
            self.balances.inc(yymm, effect)
            print 'added %s, %0.2f' % (yymm, effect)
    
    def didRemove(self, index):
        tran = self.BookSet[index]
        self.didAdd(-tran)   #invert and add
    
    def didEdit(self, index, newTran):
        oldTran = self.BookSet[index]
        self.didAdd(-oldTran)
        self.didAdd(newTran)
    
    def didChangeDrastically(self):
        self.recalc()
        
    def recalc(self):
        "Do it all quickly in one pass"    
        self.balances.clear()
        for tran in self.BookSet:
            yymm = time.gmtime(tran.date)[0:2]
            for (acct, amount, etc) in tran.lines:
                if acct == self.account:
                    self.balances.inc(yymm, amount)
    
    def getData(self):
        # numdict returns it all sorted; just need to format
        # the date column
        formatted = []
        for (period, balance) in self.balances.items():
            (year, month) = period  #unpack tuple...
            monthname = doubletalk.dates.SHORT_MONTHS[month-1]
            displayDate = monthname + '-'  + str(year)
            formatted.append((displayDate,balance))
        return formatted

    
def testView():
    bs = UserBookSet()
    bs.load('d:\\data\\project\\doubletalk\\code\\python\\doubletalk\\demodata2.dtj')  #big file 1999-2000
   
    v = MonthlyAccountActivity('MyCo.Assets.NCA.CurAss.Cash')
    bs.addView(v, 'CashBalances')
    
    print v.getDescription()
    print bs.listDelegates()
    
    import pprint
    pprint.pprint(v.getData())
    
    print 'add 25000 in January'
    tr = Transaction()
    tr.date = doubletalk.dates.asc2sec('30/1/1999')
    tr.comment = 'extra investment from Granny'
    tr.addLine('MyCo.Assets.NCA.CurAss.Cash', 25000)
    tr.addLine('MyCo.Capital.Shares', -25000)
    tr.validate()
    bs.add(tr)
    pprint.pprint(v.getData())
    
    print 'delete a transaction'
    bs.remove(0)
    pprint.pprint(v.getData())
    
        
    return tr
    

    