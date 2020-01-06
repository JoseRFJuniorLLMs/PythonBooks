#inserts

#times many insertiong methods
import ODBC.Windows
import DateTime
import time
import random
import sys


def makeData():
    # generate data
    mydata = []
    accounts = ['Cash','Fixed Assets','Income','Expenditure', 'Etc. Etc.']
    for i in range(1000):
        account = random.choice(accounts)
        amount = random.random()*1000
        theDate = DateTime.DateTime(1999,random.randint(1,12), random.randint(1,28))
        mydata.append((i + 1, theDate, account, amount))
    return mydata    


def upload(connstring='accessdemo', technique='faster'):
    if not technique in ['slow','faster','fastest']:
        print "techniques allowed: 'slow','faster','fastest'"
        return
    myconn = ODBC.Windows.connect(connstring)

    mydata = makeData()
    # clean up existing data
    mycursor = myconn.cursor()
    mycursor.execute('DELETE FROM analysis')
    mycursor.close()
    myconn.commit()

    # go
    started = time.time()
    mycursor = myconn.cursor()
        
    if technique == 'faster':
        mystatement = "INSERT INTO analysis (tranid, trandate, account, amount) VALUES(?, ?, ?, ?)"
        for row in mydata:
            mycursor.execute(mystatement, row)
        mycursor.close()
        myconn.commit()
        myconn.close()
    elif technique == 'fastest':
        mystatement = "INSERT INTO analysis (tranid, trandate, account, amount) VALUES(?, ?, ?, ?)"
        mycursor.execute(mystatement, mydata)  #all in one
        mycursor.close()
        myconn.commit()
        myconn.close()
    elif technique == 'slow':
        if connstring == 'accessdemo':
            #access can only accept whole dates in this format
            mystatement = "INSERT INTO analysis (tranid, trandate, account, amount) VALUES(%d, #%s#, '%s', %0.2f)"
            for myrow in mydata:
                mycursor.execute(mystatement % (myrow[0], str(myrow[1])[0:10], myrow[2], myrow[3]))
        else:
            #SQL standard
            mystatement = "INSERT INTO analysis (tranid, trandate, account, amount) VALUES(%d, {d '%s'}, '%s', %0.2f)"
            for myrow in mydata:
                mycursor.execute(mystatement % myrow)

        mycursor.close()
        myconn.commit()
        myconn.close()

    #done.    
    finished = time.time()
    elapsed = finished - started
    speed = len(mydata) / elapsed
    print '%s/%s:  %f/second' % (connstring, technique, speed)
    
def testJet():
    filename = 'D:\\data\\project\\oreilly\\ch13_Databases\\examples\\pydbdemos.mdb'
    mydata = makeData()
    
    import win32com.client
    myEngine = win32com.client.Dispatch('DAO.DBEngine.35')
    myDB = myEngine.OpenDatabase(filename)
    
    myDB.Execute('DELETE FROM analysis')
    started = time.time()
    mystatement = "INSERT INTO analysis (tranid, trandate, account, amount) VALUES(%d, #%s#, '%s', %0.2f)"
    for myrow in mydata:
         myDB.Execute(mystatement % (myrow[0], str(myrow[1])[0:10], myrow[2], myrow[3]))
    finished = time.time()
    elapsed = finished - started
    speed = len(mydata) / elapsed
    print 'Jet raw SQL inserts:  %f/second' % speed

    # now with AddNew/Update
    myDB.Execute('DELETE FROM analysis')
    started = time.time()
    myRS = myDB.OpenRecordset('analysis')
    for (id, date, account, amount) in mydata:
        myRS.AddNew()
        myRS.Fields('tranid').Value = id
        myRS.Fields('trandate').Value = date.COMDate()
        myRS.Fields('account').Value = account
        myRS.Fields('amount').Value = amount
        myRS.Update()
    myRS.Close()
    finished = time.time()
    elapsed = finished - started
    speed = len(mydata) / elapsed
    print 'Jet AddNew/Delete:  %f/second' % speed
    
    
    myDB.Close()
    
    
    
    

def run():
    print """This script tests insertion speed with various databases
and techniques.  1000 rows inserted into empty indexed table with
fields integer, datetime, string(100), currency.
Databases:
    Sybase Adaptive Server Anywhere, MS Access
Techniques:
    Slow:  literal statements each time
    Faster:   prepared statements issued separately (but cached...)
    Fastest:  execute(stmt, all_my_data_at_once) (loop in mxODBC)
"""
    for connstring in ['accessdemo','asademo']:
        for technique in ['slow','faster','fastest']:
            upload(connstring, technique)
    testJet()
    
if __name__ == '__main__':
        run()
    
