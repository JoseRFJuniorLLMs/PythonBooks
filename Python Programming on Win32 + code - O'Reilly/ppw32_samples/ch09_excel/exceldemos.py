# Excel demos
import win32com.client
import win32com.client.dynamic
from pywintypes import UnicodeType, TimeType

from doubletalk.bookset import BookSet
from doubletalk.transac import Transaction

import pprint
import os
import time
import string
os.chdir('c:\\data\\project\\oreilly\\ch11_excel\\examples')






class easyExcel:
    """A utility to make it easier to get at Excel.  Remembering
    to save the data is your problem, as is  error handling.
    Operates on one workbook at a time."""
    
    def __init__(self, filename=None):
        self.xlApp = win32com.client.dynamic.Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = ''  
    
    def save(self, newfilename=None):
        if newfilename:
            self.filename = newfilename
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()

    def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp
   
    def show(self):
        self.xlApp.Visible = 1
        
    def hide(self):
        self.xlApp.Visible = 0

#
#    now for the helper methods
#
    def getCell(self, sheet, row, col):
        "Get value of one cell"
        sht = self.xlBook.Worksheets(sheet)
        return sht.Cells(row, col).Value
    
    def setCell(self, sheet, row, col, value):
        "set value of one cell"
        sht = self.xlBook.Worksheets(sheet)
        sht.Cells(row, col).Value = value
    
    def getRange(self, sheet, row1, col1, row2, col2):
        "return a 2d array (i.e. tuple of tuples)"
        sht = self.xlBook.Worksheets(sheet)
        return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value
    
    def setRange(self, sheet, leftCol, topRow, data):
        """insert a 2d array starting at given location. 
        Works out the size needed for itself"""
        
        bottomRow = topRow + len(data) - 1
        rightCol = leftCol + len(data[0]) - 1
        sht = self.xlBook.Worksheets(sheet)
        sht.Range(
            sht.Cells(topRow, leftCol), 
            sht.Cells(bottomRow, rightCol)
            ).Value = data

    def getContiguousRange(self, sheet, row, col):
        """Tracks down and across from top left cell until it
        encounters blank cells; returns the non-blank range.
        Looks at first row and column; blanks at bottom or right
        are OK and return None witin the array"""
        
        sht = self.xlBook.Worksheets(sheet)
        
        # find the bottom row
        bottom = row
        while sht.Cells(bottom + 1, col).Value not in [None, '']:
            bottom = bottom + 1
        
        # right column
        right = col
        while sht.Cells(row, right + 1).Value not in [None, '']:
            right = right + 1
        
        return sht.Range(sht.Cells(row, col), sht.Cells(bottom, right)).Value
 
    def fixStringsAndDates(self, aMatrix):
        # converts all unicode strings and times
        newmatrix = []
        for row in aMatrix:
            newrow = []
            for cell in row:
                if type(cell) is UnicodeType:
                    newrow.append(str(cell))
                elif type(cell) is TimeType:
                    newrow.append(int(cell))
                else:
                    newrow.append(cell)
            newmatrix.append(tuple(newrow))
        return newmatrix
    
        
def test():
    # puts things in a new sheet which it does not save
    spr = easyExcel()
    spr.show()
    
    input = 'hello'
    spr.setCell('Sheet1',1,4, input)
    output = spr.getCell('Sheet1',1,4)
    assert input == output, 'setCell/getCell failed'
    
    input = []
    for i in range(10):
        row = []
        for j in range(4):
            row.append(str('(%dx%d)'% (j, i)))
        input.append(tuple(row))
    
    spr.setRange('Sheet1',2,2,input)
    
    output = spr.getRange('Sheet1',2,2,11,5)
    # get rid of unicode strings
    output = spr.fixStringsAndDates(output)
    assert input == output, 'setRange/getRange test failed'
    
    #get a contiguous range
    output2 = spr.getContiguousRange('Sheet1',2,2)
    dimensions = (len(output2), len(output2[0]))
    assert dimensions == (10, 4), 'getContiguousRange failed'
    
    print 'passed!'
    

def getInvoices():
    # the demo - get some data from a spreadsheet, parse it, make
    # transactions, save
    
    # step 1 - acquire the data
    spr = easyExcel('Invoices.xls')
 
    MonthEnd = int(spr.getCell('Sheet1', 3, 2))
    PreparedBy = spr.getCell('Sheet1', 4, 2)
    Submitted = int(spr.getCell('Sheet1', 5, 2))
    print 'Month end %s, prepared by %s, submitted %s' % (
                    time.ctime(MonthEnd), 
                    PreparedBy,
                    time.ctime(Submitted)
                    )
     
    # do not know how many rows
    rawInvoices = spr.getContiguousRange('Sheet1',8,1)
    rows = spr.fixStringsAndDates(rawInvoices)
    
    # check correct columns
    assert rows[0] == ('Invoice No', 'Date Raised', 
        'Customer', 'Comment', 'Category', 
        'Amount', 'Terms', 'Date Paid'
         ), 'Column structure is wrong!'
    print '%d invoices found, processing' % len(rows)
    
    # make a BookSet to hold the data
    bs = BookSet()

    # process the rows after the headings
    for row in rows[1:]:
        # unpack it into separate variables
        (invno, date, customer, comment, 
        category, fmt_amount, terms, datepaid) = row
        
        # amounts formatted as currency may be returned as strings
        amount = string.atof(fmt_amount)
        
        if date == datepaid:
            # cash payment, only one transaction
            tran = Transaction()
            tran.date = date
            tran.comment = 'Invoiced - ' + comment
            tran.customer = customer
            tran.invoiceNo = invno
            tran.addLine('MyCo.Capital.PL.Income.' + category, - amount)
            tran.addLine('MyCo.Assets.NCA.CurAss.Cash', amount)
            bs.add(tran)
            
        else:
            # need to create an invoice and a (possibly future) payment
            # first the bill    
            tran = Transaction()
            tran.date = date
            tran.comment = 'Invoiced - ' + comment
            tran.customer = customer
            tran.invoiceNo = invno
            tran.addLine('MyCo.Capital.PL.Income.' + category, - amount)
            tran.addLine('MyCo.Assets.NCA.CurAss.Creditors', amount)
            bs.add(tran)
     

            # now the payment.  If not paid, use the terms to estimate a
            # date, and flag it as a Scheduled transaction (i.e. not real)
            tran = Transaction()
            if datepaid == None:
                datepaid = date + (terms * 86400)
                tran.mode = 'Scheduled'    # tag it as not real
            tran.date = date
            tran.comment = 'Invoice Paid - ' + comment
            tran.customer = customer
            tran.invoiceNo = invno
            tran.addLine('MyCo.Assets.NCA.CurAss.Creditors', - amount)
            tran.addLine('MyCo.Assets.NCA.CurAss.Cash', amount)
            bs.add(tran)
     
    # we're done, save and pack up
    filename = 'invoices.dtj'
    bs.save(filename)
    print 'Saved in file', filename
    spr.close()
    
            
        
     