# Doubletalk COM servers
"""This module exposes COM servers for both Transaction and BookSet.

"""

import doubletalk.transac
import doubletalk.bookset
import doubletalk.userhooks

from win32com.server.exception import COMException
import win32com.server.register
import win32com.server.util
import win32com.client.dynamic

from pywintypes import UnicodeType  #used in checking type of user expressions
import string    #used in standard output handling
import sys
import os


class COMTransaction:
    # we don't need all the _reg_ stuff, as we provide our own
    # API for creating these and do not use the registry.
    _public_methods_ = [
                'asString',
                'getDateString',
                'setDateString',
                'setCOMDate',
                'getCOMDate',
                'getComment',
                'setComment',
                'getLineCount',
                'getAccount',
                'getAmount',
                'addLine',
                'addLastLine',
                'getOneLineDescription'
                ]
    
    def __init__(self, tran=None):
        if tran is None:
            self._tran = doubletalk.transac.Transaction()
        else:
            self._tran = tran       
        
    def asString(self):
        return self._tran.asString()
    
    def getDateString(self):
        return self._tran.getDateString()
    
    def setDateString(self, aDateString): 
        self._tran.setDateString(str(aDateString))
    
    def setCOMDate(self, comdate):
        self._tran.date = (comdate - 25569.0) * 86400.0
        
    def getCOMDate(self):
        return (self._tran.date / 86400.0) + 25569.0

    def getComment(self):
        return self._tran.comment

    def setComment(self, aComment):
        self._tran.comment = str(aComment)
       
    def getOneLineDescription(self):
        return '%-15s %s %10.2f' % (
            self._tran.getDateString(), 
            self._tran.comment,
            self._tran.magnitude()
            )
    
    def getLineCount(self):
        return len(self._tran.lines)
    
    def getAccount(self, index):
        return self._tran.lines[index][0]
        
    def getAmount(self, index):
        return self._tran.lines[index][1]
    
    def addLine(self, account, amount):
        self._tran.addLine(str(account), amount)
       
    def addLastLine(self, account):
        self._tran.addLastLine(str(account))

        
class COMBookSet:
    _reg_clsid_ = '{38CB8241-D698-11D2-B806-0060974AB8A9}'
    _reg_desc_ = 'Doubletalk BookServer'
    _reg_progid_ = 'Doubletalk.BookServer'
    _reg_class_spec_ = 'doubletalk.comservers.COMBookSet'
    _public_methods_ = [
                'double',
                'interpretString',  # tries exec, then eval
                'execFile',
                'importFile',
                'beginTrappingOutput', 
                'endTrappingOutput', 
                'getStandardOutput',
                'getViewData',
                'count',
                'createTransaction',
                'getTransaction','getTransactionString',
                'getOneLineDescription',
                'load', 'loadFromText', 'loadFromString',
                'save', 'saveAsText', 'asString',
                'edit','add',
                'getAccountDetails',
                'getAccountList',
                'drawAccountChart',
                'doDelphiCallbackDemo'

        ]
    
    def __init__(self):
        #self.__BookSet = doubletalk.bookset.BookSet()
        self.__BookSet = doubletalk.userhooks.UserBookSet()

        # create a custom namespace for the user to work with
        self.userNameSpace = {'TheBookSet': self.__BookSet}

    
    ######################################################
    #             
    # utilities
    #
    ######################################################
    
    def double(self, arg):
        # trivial test function to check it is live
        return arg * 2
    
    def count(self):
        # return number of transactions
        return len(self.__BookSet)
    
    def getTransaction(self, index):
        python_tran = self.__BookSet[index]
        com_tran = COMTransaction(python_tran)
        return win32com.server.util.wrap(com_tran)
        
    def getOneLineDescription(self, index):
        tran = self.__BookSet[index]
        return '%-15s %s %10.2f' % (
            tran.getDateString(), 
            tran.comment,
            tran.magnitude()
            )
    
    def getTransactionString(self, index):
        return self.__BookSet[index].asString()
       
    def createTransaction(self):
        comTran = COMTransaction()
        idTran = win32com.server.util.wrap(comTran)
        return idTran
        
    ######################################################
    #             
    # start off with open/save functionality
    #
    ######################################################
    
    def load(self, filename):
        self.__BookSet.load(str(filename))
            
    def loadFromText(self, filename):
        self.__BookSet.loadFromText(str(filename))
    
    def loadFromString(self, bigstring):
        self.__BookSet.loadFromString(str(bigstring))
    
    def save(self, filename):
        self.__BookSet.save(str(filename))
        
    def saveAsText(self, filename):
        self.__BookSet.saveAsText(str(filename))
    
    def asString(self):
        return self.__BookSet.asString()

    def add(self, idTran):
        comTran = win32com.server.util.unwrap(idTran)
        pyTran = comTran._tran
        self.__BookSet.add(pyTran)
        
    def remove(self, index):
        self.__BookSet.remove(index)
    
    def edit(self, index, idTran):
        comTran = win32com.server.util.unwrap(idTran)
        pyTran = comTran._tran
        self.__BookSet.edit(index, pyTran)



    ######################################################
    #             
    # dynamic interpretation
    #
    ######################################################

    
    
    def interpretString(self, expr):
        """Makes it easier to build consoles.
        """

        open('c:\\booksetlog.txt','a').write('interpretString:' + str(expr) + '\n')
        
        if type(expr) not in [type(''), UnicodeType]:
            raise Exception(desc="Must be a string",scode=winerror.DISP_E_TYPEMISMATCH)
        try: 
            # first, we assume it is an expression
            result_object = eval(str(expr), self.userNameSpace)
            if result_object == None:
                return ''
            else:
                return str(result_object)
        except:
            #failing that, try to execute it
            exec str(expr) in self.userNameSpace
            return ''

    def execFile(self, filename):
        if type(filename) not in [type(''), UnicodeType]:
            raise Exception(desc="Must be a string",scode=winerror.DISP_E_TYPEMISMATCH)
        execfile(str(filename), self.userNameSpace)
        
    def importFile(self, fullpathname):
        #import as the filename
        import imp
        path, filename = os.path.split(str(fullpathname))
        root, ext = os.path.splitext(filename)
        found = imp.find_module(root, [path])  #takes a list of files
        if found:
            (file, pathname, description) = found
            try:
                module = imp.load_module(root, file, pathname, description)
                # ensure it is visible in our namespace
                self.userNameSpace[root] = module
                
                print 'loaded module', root
            finally:
                file.close()    
        else:
            print 'file not found'
        
                

    def beginTrappingOutput(self):
        self.outputBuffer = []
        self.old_output = sys.stdout
        sys.stdout = self
    
    def write(self, expr):
        """ this is an internal utility used to trap the output.
        add it to a list of strings - this is more efficient
        than adding to a possibly very long string."""
        self.outputBuffer.append(str(expr))

    def getStandardOutput(self):
        "Hand over output so far, and empty the buffer"
        text = string.join(self.outputBuffer, '')
        self.outputBuffer = []
        return text

    def endTrappingOutput(self):
        sys.stdout = self.old_output
        # return any more output
        return self.getStandardOutput()


    ######################################################
    #             
    # basic views
    #
    ######################################################
    
    #only use this is based on UserBookSet
    def getViewData(self, viewName):
        return self.__BookSet.getViewData(str(viewName))
        
    def getAccountDetails(self, match):
        return self.__BookSet.getAccountDetails(str(match))
        
    def getAccountList(self):
        return self.__BookSet.getAccountList()

        
    ######################################################
    #             
    # callback graphics
    #
    ######################################################
    def drawAccountChart(self, vbForm):
        """Draws a chart on the VB form.  Bad design as it ties the back end to VB,
        but demonstrates most features involved in callbacks. It also includes some
        print statements which will show up in the Trace Collector debugging tool -
        this tool is essential for debugging."""

        print 'Drawing chart...'
        from doubletalk.dates import *
        import time
        
        # Make a Dispath wrapper around the vb Form object so we can call
        # any of its methods.
        idForm = win32com.client.Dispatch(vbForm)
        

        # call a method we defined on the VB form        
        # arrays are converted automatically to Python tuples we can access
        (width, height) = idForm.GetClientArea()
        account = idForm.GetAccount()        

        # access a built-in property of the VB form
        idForm.Caption = "Account " + account

        #############################################################
        # now for the chart drawing - calling our own VB methods...
        #############################################################
        
        idForm.ClearChart()    #clear the form

        # if the area is too small to do anything with, exit
        if width < 1440:
            return
        if height < 1440:
            return
        
        #work out the inner drawing rectangle
        plotrect = (720,720, width-720, height - 720)
        
        # draw a blue bounding rectangle
        idForm.DrawBox(plotrect[0], plotrect[1], plotrect[2], plotrect[3], 0xFF0000, 0xFFFFFF)
        
        
        #fetch the account data
        data = self.__BookSet.getAccountDetails(account)
        if len(data) == 0:
            idForm.DrawText(720, 200, 12, 'No Account Specified')
            return
        
        idForm.DrawText(720, 200, 12, 'Chart of account ' + account)
        
        #work out the boundaries and scale factors
        startDate = asc2sec(data[0][1])
        endDate = asc2sec(data[-1][1])
        
        xscale = (width - 1440.0) / (1.0 * endDate - startDate)
        
        print 'plot rect =', plotrect
        print 'start date = %d, end date = %d' % (startDate, endDate)
        print 'x zero = %0.2f, x scale factor = %f' % (plotrect[0], xscale)
        
        #get min and max balances to occur
        maxvalue = 0
        minvalue = 0
        for row in data:
            if row[4] > maxvalue:
                maxvalue = row[4]
            if row[4] < minvalue:
                minvalue = row[4]
        if maxvalue == minvalue:
            return
        print 'data min=%f, max=%f' % (minvalue, maxvalue)
        
        yzero = int(plotrect[1] + ((plotrect[3] - plotrect[1]) * maxvalue / (maxvalue - minvalue)))
        yscale = (plotrect[3] - plotrect[1]) / (maxvalue - minvalue)
        
        print 'y zero = %0.2f, y scale factor = %0.2f' % (yzero, yscale)
        
        #label the axes crudely
        idForm.DrawText(plotrect[0], plotrect[3], 8, sec2asc(startDate))
        idForm.DrawText(plotrect[2] - 360, plotrect[3], 8, sec2asc(endDate))
        
        idForm.DrawText(100, plotrect[1], 8, str(int(maxvalue)))
        idForm.DrawText(100, yzero - 100, 8, '0')
        idForm.DrawText(100, plotrect[3] - 200, 8, str(int(minvalue)))
        
        #draw x axis
        idForm.DrawLine(plotrect[0], yzero, plotrect[2], yzero, 0x00)        
        
        #loop over each point
        prev_x = plotrect[0]
        
        for row in data:
            date = asc2sec(row[1])
            value = row[4]
            x = int(plotrect[0] + xscale * (date-startDate))
            y = int(yzero - yscale * value)
            #draw a box - black above line, red below
            if value > 0:
                color = 0x00  #black
            else:
                color = 0xFF  #red
            print 'date=%d, value = %0.2f, x=%d, y=%d, isblack=%d' % (date, value, x, y, value>0)    
            idForm.DrawBox(prev_x, yzero, x, y, color, color)
            prev_x = x
            
    def doDelphiCallbackDemo(self, delphiTextBox):
        idTextBox = win32com.client.dynamic.Dispatch(delphiTextBox)
        idTextBox.Text = 'Python was here!';
        

def TestDirect():
    tran = COMTransaction()
    four = tran.double(2)
    print '2 * 2 =',four
    assert four == 4, 'COMTransaction not working'

def TestCOM():
    #try:
    comtran = win32com.client.dynamic.Dispatch("Doubletalk.Transaction")
    #    print 'COM Transaction object created'
    #except:
    #    print "**** - The Doubletalk Transaction is not available - ****"
    #    return
    four = comtran.double(2)
    print '2 * 2 =',four
    assert four == 4, 'COMTransaction not working'


if __name__ == '__main__':
    win32com.server.register.UseCommandLine(COMBookSet)