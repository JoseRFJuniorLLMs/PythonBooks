# basic printing demonstration

import win32ui
import win32con

myprinter = "HP DeskJet 820C Series Printer"   # get the name from the Printers folder

def print_it():
	
	dc = win32ui.CreateDC()
	dc.CreatePrinterDC()   # ties it to your default printer
	
	dc.StartDoc('My Python Document')
	#dc.SetMapMode(win32con.MM_LOENGLISH)
	
	dc.StartPage()

		
	
	# text - near the top left corner somewhere	
	dc.TextOut(110,790, 'Hello, World')  # 1 inch in, 8 up
	
	# try to draw a box around it - not device-specific
	dc.MoveTo(100,800)
	dc.LineTo(400,800)
	dc.LineTo(400,700)
	dc.LineTo(100,700)
	dc.LineTo(100,800)
	
	
	dc.EndPage()
	dc.EndDoc()
	print 'sent to printer'
	
	del dc
	
	
	