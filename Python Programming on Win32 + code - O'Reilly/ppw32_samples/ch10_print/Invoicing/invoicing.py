# invoicing.py
"""This is an example for the PDFgen library.  It prints a series of
invoices.  The data is prepared in a tab-delimited text file with the field
names in the first row.  The system generates a PDF file for each invoice
and writes it to disk. In real life it would add transactions to a BookSet
as well."""


import string
from doubletalk.dates import asc2sec, ddmmmyyyy
from piddle import *
import pdfcanvas

INCH = 72    

def run():
    import os
    os.chdir('c:\\data\\project\\oreilly\\ch12_print\\examples')
    
    invoices = acquireData()
    print 'loaded data'
    for invoice in invoices:
        printInvoice(invoice)
    print 'Done'

    
class InvoiceRec:
    pass  # dummy class to hang variables off

def acquireData():
    # do your stuff here - it could come from business objects,
    # flat files, spreadsheets or databases.  We've provided a
    # text file with ready-to-use data
    lines = open('Invoicing.dat','r').readlines()
    data = []
    for line in lines:
        line = line[:-1]   # chop off newline
        words = string.split(line, ',')  # tab-delimited
        data.append(words)
    
    
    # now turn it into dictionaries - easier to read    
    header = data[0]
    body = data[1:]
    cols = len(header)
    
    invoices = []
    for row in body:
        customer = InvoiceRec()
        for col in range(cols):
            fieldname = header[col]
            value = row[col]

            #get the right type for each field
            if fieldname in ['InvoiceID','Hours','HourlyRate','Expenses', 'TaxRate']:
                value = string.atof(value)
            elif fieldname in ['InvoiceDate', 'PeriodEnding']:
                value = asc2sec(value)

            setattr(customer, fieldname, value)
        invoices.append(customer)
    return invoices


def printInvoice(inv):
    #first see what to call it
    
    filename = 'INVOICE_%d_%s.PDF' % (inv.InvoiceID, inv.ClientID)
    canv = pdfcanvas.PDFCanvas(filename)
    
    #make up the standard fonts we need and attach to the canvas
    canv.standardFont = pdfcanvas.Font(face='Helvetica',size=12)
    canv.boldFont = pdfcanvas.Font(face='Helvetica',bold=1, size=12)
        
    #now all the static repeated elements
    drawHeader(canv, filename)
    drawOwnAddress(canv)
    
    # now all the data elements
    drawGrid(canv, inv)
    drawCustomerAddress(canv, inv)
    drawInvoiceDetails(canv, inv)
    
    #save
    canv.flush()
    
    
    
def drawHeader(canv, filename):
    # border down one side
    canv.drawLine(0.8*INCH , INCH/2, 0.8*INCH, 11*INCH, 
                    color=blue, width=6)

    #put a very small filename near top left
    fnt = pdfcanvas.Font(face='Helvetica',size=5,italic=1)
    canv.drawString(filename, INCH, INCH/2, font=fnt)
    
    #attempt at word art - stagger two colours over each other
    fnt = pdfcanvas.Font(face='Helvetica',size=INCH/2,bold=1,italic=1)
    shades = [red,green,yellow,blue]  #all defined in piddle and pdfcanvas
    for i in range(len(shades)):
        canv.drawString('Pythonics Ltd.', INCH+2*i, INCH+2*i, fnt, color=shades[i])
    
    #the word 'invoice'
    canv.drawString('Invoice', 5.4 * INCH, INCH, fnt)
    
def drawOwnAddress(canv):
    address = ['Village Business Centre',
            'Thornton Hill',
            'Wimbledon Village',
            'London SW19 8PY',
            'Tel +44-181-123-4567']
    fnt = Font(face='Helvetica',size=12,italic=1)
    canv.drawStrings(address, INCH, INCH * 1.5, fnt)
    
 
def drawCustomerAddress(canv, inv):
    canv.drawString('To:', INCH, 3.0 * INCH, font=canv.boldFont)
    their_address = []
    for line in [inv.ContactName, inv.CompanyName, 
                inv.Address1, inv.Address2, inv.Address3, inv.Address4]:
           if line <> '':
                their_address.append(line)
    canv.drawStrings(their_address, INCH * 1.5, INCH * 3.0)


def drawInvoiceDetails(canv, inv):
    # invoice no and date
    canv.drawString('Invoice No:', INCH * 5.2, INCH * 3.0, font=canv.boldFont)
    canv.drawString('%d' % inv.InvoiceID, INCH * 6.25, INCH * 3.0, font=canv.boldFont)
    canv.drawString('Date:', INCH * 5.2, INCH * 3.2, font=canv.boldFont)
    canv.drawString(ddmmmyyyy(inv.InvoiceDate), INCH * 6.25, INCH * 3.2, font=canv.boldFont)
    
    
def drawGrid(canv, inv):
    xlines = [INCH, 2*INCH, 5.27*INCH, 6.27*INCH, 7.27*INCH]
    ylines = [4.0 * INCH, 4.3 * INCH, 4.6 * INCH, 
            4.9 * INCH, 5.2 * INCH, 5.5 * INCH, 5.8 * INCH]
    
    #draw the main grid, slightly shaded upper
    canv.drawRect(xlines[0], ylines[0], xlines[4],ylines[1],
        fillColor=Color(0.9,0.9,0.9), closed=1)
    for x in xlines:
        canv.drawLine(x,ylines[0], x, ylines[3])
    for y in ylines[0:4]:
        canv.drawLine(xlines[0], y, xlines[-1], y)
    
    #and the bottom right one for totals
    for x in xlines[3:]:
        canv.drawLine(x,ylines[3], x, ylines[6])
    for y in ylines[4:7]:
        canv.drawLine(xlines[3], y, xlines[-1], y)
        
    # put the titles in
    canv.drawString('Quantity', xlines[0] + 12, ylines[1] - 6, canv.boldFont)
    canv.drawString('Description', xlines[1] + 12, ylines[1] - 6 , canv.boldFont)
    canv.drawString('Unit Price', xlines[2] + 12, ylines[1] - 6 ,  canv.boldFont)
    canv.drawString('Amount', xlines[3] + 12, ylines[1] - 6 , canv.boldFont)
    
    # and the data
    fntSmall = Font(face='Helvetica', size=10)
    strHours = '%0.2f hours' % inv.Hours
    canv.drawString(strHours, xlines[0] + 12, ylines[2] - 6, fntSmall)
    
    strDescr = 'Consulting work for week ending ' + ddmmmyyyy(inv.PeriodEnding)
    canv.drawString(strDescr, xlines[1] + 12, ylines[2] - 6, fntSmall)
    
    strUnitPrice = '£%0.2f/hr' % inv.HourlyRate
    canv.drawString(strUnitPrice, xlines[2] + 12, ylines[2] - 6, fntSmall)
    
    labour = inv.HourlyRate * inv.Hours
    strLabour = '£%0.2f' % labour
    canv.drawString(strLabour, xlines[3] + 12, ylines[2] - 6, fntSmall)
    
    if inv.Expenses > 0.001:
        canv.drawString('Expenses: ' + inv.ExpenseDetails, xlines[1] + 12, ylines[3] - 6, fntSmall)
        canv.drawString('£%0.2f' % inv.Expenses, xlines[3] + 12, ylines[3] - 6, fntSmall)
    net = labour + inv.Expenses
    strNet = '£%0.2f' % net
    canv.drawString(strNet, xlines[3] + 12, ylines[4] - 6, fntSmall)
    canv.drawString('Net:', xlines[2] + 12, ylines[4] - 6, fntSmall)
    
    tax = net * inv.TaxRate
    strTax = '£%0.2f' % tax
    canv.drawString(strTax, xlines[3] + 12, ylines[5] - 6, fntSmall)
    canv.drawString('Tax:', xlines[2] + 12, ylines[5] - 6, fntSmall)
    
    gross = net + tax
    strGross = '£%0.2f' % gross
    canv.drawString(strGross, xlines[3] + 12, ylines[6] - 6, fntSmall)
    canv.drawString('Gross:', xlines[2] + 12, ylines[6] - 6, fntSmall)
    
def drawComment():
    canv.drawString(inv.Comment, 7 * INCH, 2 * INCH)

if __name__ == '__main__':
    run()
    