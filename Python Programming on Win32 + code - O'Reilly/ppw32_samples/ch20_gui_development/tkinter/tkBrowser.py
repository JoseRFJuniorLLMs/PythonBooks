
# This application implements a browser for doubletalk booksets.  If
# can present any number of views of any number of booksets in a
# reasonably standard Document/View model.  Each view is in a separate
# top level window.  There are three types of views:

#  Journal view -- shows all transactions, one per line.

#  Detail account view -- shows all transactions which effect a given account.

#  Account graph view -- Graphs a running balance of a given account.

# New views of any type can be created easily.  Journal views can open
# new booksets.  Either of the account views can use an option menu to
# change to a different account.

# Double clicking on a transaction in any view (or selecting the
# transaction and choosing the "Edit->Edit Selected Transaction" menu
# item) will open an "Edit Transaction" dialog.  Similarly the
# "Edit->Create New Transaction" will open an empty "Edit Transaction"
# dialog.

# In the "Edit Transaction" dialog, the date and comment can be
# edited, and line items can be edited, added, or deleted.  (Slightly
# unconventionally, the line at which the deletion occurs or after
# which insertion occurs is the line whose amount column currently has
# the keyboard focus.)  Validation code on all fields and on the
# transaction sum is run when the OK button is hit.  Any problems are
# reported and the OK button push is ignored.  On successful
# completion, the edited/new transaction is entered into the bookset,
# and all views of that bookset are immediately updated.

# This  file consist of the following sections:

# Imports and constants	 -- 
# class AugmentedBookset -- A doubletalk Bookset with added file functionality.
# class ScrolledListbox	 -- A complex widget formed from  simple widgets.
# class View			 -- Base class for each of the three view classes.
# class JournalView		 -- An implementation of one view.
# class AccountView		 -- An implementation of another view.
# class AccountGraph	 -- An implementation of yet another view.
# class EditTransaction	 -- The edit Transaction dialog
# Main Application		 -- Commandline parser and main interactive loop call.


######################################################################
## Imports and constants
######################################################################

import sys, string

from doubletalk.bookset import BookSet
from doubletalk.transac import Transaction
from doubletalk.dates import asc2sec

from Tkinter import *
import tkMessageBox
import tkFileDialog
import tkSimpleDialog

Root = Tk()
Root.withdraw()

FONT = 'Courier 9'
FILETYPES = [('Doubletalk Journal', '*.dtj'), ('All files', '*')]

AboutMessage = '''Doubletalk Browser
using the Tkinter GUI

by

Dr. Gary Herron
gjh@aw.sgi.com'''


######################################################################
## class AugmentedBookset
######################################################################

class AugmentedBookset(BookSet):
	
	''' A doubletalk bookset with several additions: Its associated
	filename, an edited/not-edited flag, and methods for saving or
	asking the users desire to quit without saving an edited
	bookset.'''
	
	def __init__(self, filename=''):
		BookSet.__init__(self)
		self.__filename = filename
		self.__edited = 0
		if filename:
			self.load(self.__filename)
			
	def Edited(self):  return self.__edited
	def Changed(self):  self.__edited = 1
	
	def Save(self):
		if self.__filename:
			self.save(self.__filename)
			self.__edited = 0
		else:
			self.SaveAs()
			
	def SaveAs(self):
		name = tkFileDialog.asksaveasfilename(filetypes=FILETYPES,
											  initialfile=self.__filename)
		if name:
			self.__filename = name
			self.Save()
			
	def querySave(self):
		r = tkMessageBox.askyesno('Bookset not saved',
								  'Bookset is not saved.\n\nClose anyway?')
		if r:
			self.__edited = 0
		else:
			self.SaveAs()
			
	
######################################################################
## class ScrolledListbox
######################################################################

class ScrolledListbox(Frame):

	''' A listbox widget with an associated scrollbar and a label, all
	packed into a single frame widget.  This single frame widget is
	made to act like a listbox delegation.  We only delegate the few
	listbox methods we actually use.  A true implementation would need
	to be more thorough.

	Note: The label placed across the top of the listbox is
	implemented with a single line Listbox rather than the Label
	widget.  Why?  The registration betweem columns of the label and
	the listbox is lost when the window is resized because the Listbox
	and Label widget have different resize behavior.  However tow
	Listbox widgets initially lined up stay lined up through resize. '''

	def __init__(self, master, labelText=None, **kw):
		Frame.__init__(self, master, relief=GROOVE, bd=4)

		label = Listbox(self, width=len(labelText), height=1,
						font=FONT, relief=FLAT,
						selectbackground='gray', selectborderwidth=0,
						selectforeground='black')
		label.insert(AtEnd(), labelText)
		
		kw['width'] = len(labelText)
		self.listbox = Listbox(self, kw)

		scrollbar = Scrollbar(self)
		self.listbox.configure(yscrollcommand=(scrollbar, 'set'))
		scrollbar.configure(command=(self.listbox, 'yview'))

		label.pack(side=TOP, fill=X)
		self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)
		scrollbar.pack(side=LEFT, fill=Y)
		
	def insert(self, *args): return apply(self.listbox.insert, args)
	def delete(self, *args): return apply(self.listbox.delete, args)
	def bind(self, *args): return apply(self.listbox.bind, args)
	def curselection(self): return self.listbox.curselection()


######################################################################
## class View
######################################################################

class View(Toplevel):

	''' The base class for all the view classes.  It keeps track of
	all the ixisting views in a class variable "viewList".  When the
	last view is closed, the application is terminated.  The methods
	provided by this class fall into three categories.

	Initialization methods:
		The __init__ method is its helper CreateMenubar method.

	Bookset and account association and display methods:
		Methods to make or break the association between a view and
		the bookset (and when necessary, the specific account) to be
		displayed.

	Menu handling methods:
		A batch of short methods called in response to user choice of
		menu items.

	'''
	
	viewList = []

    #
	# Initialization methods
	#
	def __init__(self, bookset, needsAccount=None):
		Toplevel.__init__(self)
		self.protocol('WM_DELETE_WINDOW', self.Close)
		
		self.needsAccount = needsAccount
		self.bookset = None
		self.account = StringVar()
		
		self.CreateMenubar()
		
		self.viewList.append(self)
		if bookset:
			self.setBookset(bookset)
		self.focus_set()

	def CreateMenubar(self):
		menubar = Menu(self)
		self.config(menu=menubar)

		# File menu
		filemenu = Menu(menubar)
		menubar.add_cascade(label='File', menu=filemenu)
		filemenu.add_command(label='New', command=self.New)
		if not self.needsAccount:
			filemenu.add_command(label='Open ...', command=self.Open)
		filemenu.add_separator()
		filemenu.add_command(label='Save', command=self.Save)
		filemenu.add_command(label='Save as ...', command=self.SaveAs)
		filemenu.add_separator()
		filemenu.add_command(label='Close', command=self.Close)
		filemenu.add_command(label='Exit', command=self.Exit)

		# View menu
		viewmenu = Menu(menubar)
		menubar.add_cascade(label='View', menu=viewmenu)
		viewmenu.add_command(label='Journal View',
							 command=self.createJournalView)
		viewmenu.add_command(label='Account View',
							 command=self.createAccountView)
		viewmenu.add_command(label='Graph View',
							 command=self.createGraphView)

		# Edit menu
		editmenu = Menu(menubar)
		menubar.add_cascade(label='Edit', menu=editmenu)
		editmenu.add_command(label='Edit Selected Transacton',
							 command=self.editTransaction)
		editmenu.add_command(label='Create New Transaction',
							 command=self.createTransaction)

		# Help menu
		helpmenu = Menu(menubar)
		menubar.add_cascade(label='Help', menu=helpmenu)
		helpmenu.add_command(label='About', command=self.About)

		if self.needsAccount:
			self.accFrame = Frame(self)
			self.accFrame.pack(side=TOP, expand=YES, fill=X)
			Label(self.accFrame, text='Account:').pack(side=LEFT)

	#
	# Bookset and account association and display methods:
	#
	def setBookset(self, bookset):
		if not self.unsetBookset(): return
		self.bookset = bookset

		if self.needsAccount:
			accmenu = apply(OptionMenu, [self.accFrame, self.account, ''] \
							+ self.bookset.getAccountList())
			accmenu.configure(width=45)
			accmenu.pack(side=LEFT)
			accmenu.bind('<ButtonRelease-1>', self.setAccount) # Windows
			accmenu['menu'].bind('<ButtonRelease-1>', self.setAccount) # Unix

	def unsetBookset(self):
		if not self.bookset:  return 1
		
		if self.isLastViewOfBookset() and self.bookset.Edited():
			self.bookset.querySave()
			if self.bookset.Edited(): return 0
			
		self.bookset = None
		self.DisplayView()
		return 1

	def setAccount(self, event=None):
		self.after(0, self.DisplayView)

	def isLastViewOfBookset(self):
		booksetList = map(lambda view: view.bookset, self.viewList)
		return booksetList.count(self.bookset) == 1

	def Display(self):
		pass

	def DisplayAllViewsOfBookset(self, bookset):
		for view in self.viewList:
			if view.bookset == bookset:
				view.DisplayView()

	#	
	# Menu handling methods:
	#
	def New(self):
		JournalView()

	def Open(self):
		name = tkFileDialog.askopenfilename(filetypes=FILETYPES)
		if name:
			self.setBookset(AugmentedBookset(name))
			self.DisplayView()

	def Save(self):
		if self.bookset:  self.bookset.Save()

	def SaveAs(self):
		if self.bookset:  self.bookset.SaveAs()

	def Close(self):
		if not self.unsetBookset(): return
		self.viewList.remove(self)
		self.destroy()
		if not self.viewList:
			sys.exit()

	def Exit(self):
		for view in self.viewList[:]:
			view.Close()
		
	def createJournalView(self):
		JournalView(self.bookset)

	def createAccountView(self):
		AccountView(self.bookset, self.account.get())

	def createGraphView(self):
		AccountGraph(self.bookset, self.account.get())

	def editTransaction(self):
		pass

	def createTransaction(self):
		pass

	def About(self):
		tkMessageBox.showinfo('About tkBrowser', AboutMessage)


######################################################################
## class JournalView
######################################################################

class JournalView(View):

	''' Presents a list of one-line summaries, one for each
	transaction in a bookset.  Double clicking on a line will bring up
	the "Edit Transaction" dialog on that transaction. '''

	dataFormat = '%11s  %-45s %10.2f'
	labelFormat ='%11s  %-45s %10s'
	labelText = labelFormat % ('Date','Comment','Amount')
	
	def __init__(self, bookset=None):
		View.__init__(self, bookset)
		self.title('Journal View')

		self.listbox = ScrolledListbox(self, self.labelText,
									   height=20, font=FONT)
		self.listbox.pack(side=TOP, expand=YES, fill=BOTH)
		self.listbox.bind('<Double 1>', self.editTransaction)
		self.DisplayView()

	def DisplayView(self):
		self.listbox.delete(0, AtEnd())
		if not self.bookset: return
		strings = map(lambda tr, format=self.dataFormat:
						format%(string.split(tr.getDateString())[0],
								tr.comment,
								tr.magnitude()),
				   self.bookset)
		apply(self.listbox.insert, [AtEnd()]+ strings)

	def editTransaction(self, event=None):
		try:
			index = string.atoi(self.listbox.curselection()[0])
		except IndexError:
			index = None
		EditTransaction(self.bookset, index)
		self.DisplayAllViewsOfBookset(self.bookset)

	def createTransaction(self, event=None):
		EditTransaction(self.bookset, None)
		self.DisplayAllViewsOfBookset(self.bookset)


######################################################################
## class AccountView
######################################################################

class AccountView(View):

	''' Presents a detailed view of all the transactions which affect
	a given# account.  This view may be initially blank if invoked
	from a Journal view (since such a view has no specific account).
	The account may be (re)specified at any time via an option menu.
	Double clicking on a line will bring up the "Edit Transaction"
	dialog on that transaction. '''

	dataFormat = '%5d %11s  %-45s %10.2f %10.2f'
	labelFormat ='%-5s %11s  %-45s %10s %10s'
	labelText = labelFormat % ('Index','Date','Comment','Amount','Balance')
	
	def __init__(self, bookset, account=None):
		View.__init__(self, bookset, needsAccount=1)
		self.title('Detailed Account View')

		self.account.set(account)

		self.listbox = ScrolledListbox(self, self.labelText, font=FONT,
									   height=20)
		self.listbox.pack(side=TOP, expand=YES, fill=BOTH)
		self.listbox.bind('<Double 1>', self.editTransaction)
		self.DisplayView()

	def DisplayView(self):
		self.listbox.delete(0, AtEnd())
		if not self.bookset or not self.account.get(): return

		accountDetails = self.bookset.getAccountDetails(self.account.get())
		for index,date,comment,amount,balance in accountDetails:
			self.listbox.insert(AtEnd(), self.dataFormat \
								%(index,date,comment[:45],amount,balance))

	def editTransaction(self, event=None):
		index = string.atoi(self.listbox.curselection()[0])
		index = self.bookset.getAccountDetails(self.account.get())[index][0]
		EditTransaction(self.bookset, index)
		self.DisplayAllViewsOfBookset(self.bookset)

	def createTransaction(self, event=None):
		EditTransaction(self.bookset, None)
		self.DisplayAllViewsOfBookset(self.bookset)


######################################################################
## class AccountGraph
######################################################################

class AccountGraph(View):

	''' Presents a graphical view of the running balance of a
	particular account.  This view may be initially blank if invoked
	from a Journal view (since such a view has no specific account).
	The account may be (re)specified at any time via an option
	menu. '''

	def __init__(self, bookset, account):
		View.__init__(self, bookset, needsAccount=1)
		self.title('Account Graph')

		self.account.set(account)

		self.content = Canvas(self, width=600, height=300, relief=GROOVE, bd=4)
		self.content.bind('<Configure>', self.DisplayView)
		self.content.pack(side=TOP, expand=YES, fill=BOTH)
		self.DisplayView()

	def DisplayView(self, *args):
		self.content.delete('all')
		if not self.bookset or not self.account.get(): return

		width,height = self.content.winfo_width(), self.content.winfo_height()
		if width <= 1 or height <= 1: return

		wx0, wy0 = 90.0, height-40.0
		wx1, wy1 = width-10.0, 20.0
		
		accountDetails = self.bookset.getAccountDetails(self.account.get())
		if len(accountDetails) < 2: return
		balanceList = map(lambda d: d[4], accountDetails) + [0.0]
		
		startTime, stopTime = accountDetails[0][1], accountDetails[-1][1]
		startBalance = accountDetails[0][4]

		x0, y0 = asc2sec(startTime),  min(balanceList)
		x1, y1 = asc2sec(stopTime), max(balanceList)

		xs, ys = (wx1-wx0)/(x1-x0), (wy1-wy0)/(y1-y0)
		xz, yz = (wx0*x1-wx1*x0)/(x1-x0), (wy0*y1-wy1*y0)/(y1-y0)

		xp, yp = xz + xs*x0, yz + ys*startBalance

		cx0, cy0 = xz + xs*x0, yz + ys*y0
		cx1, cy1 = xz + xs*x1, yz + ys*y1

		self.content.create_text(cx0-10,yz, text='0.00',
								 anchor=E, font=FONT)
		self.content.create_text(cx0-10,cy0, text='%8.2f'%y0,
								 anchor=E, font=FONT)
		self.content.create_text(cx0-10,cy1, text='%8.2f'%y1,
								 anchor=E, font=FONT)
		self.content.create_text(cx0,cy0+10, text=startTime,
								 anchor=NW, font=FONT)
		self.content.create_text(cx1,cy0+10, text=stopTime,
								 anchor=NE, font=FONT)
		
		self.content.create_line(cx0,cy1, cx0,cy0, cx1, cy0)

		for index,date,comment,amount,balance in accountDetails:
			x, y = xz + xs*asc2sec(date), yz + ys*balance
			self.content.create_rectangle(xp,yz, x,yp,
										  outline='black', fill='black')
			xp, yp = x, y


######################################################################
## class EditTransaction
######################################################################

class EditTransaction(tkSimpleDialog.Dialog):

	''' Display a (possibly blank) transaction and allow any of the
	fields to be edited.  Also, allow transaction-amount lines to be
	added/deleted/edited.  When the OK button is pushed, all fields
	are validated and the sum is verified to be zero.  Any failure is
	reported and the dialog is not dismissed until the user gets it
	right or cancels.  On success, the original transaction (if any)
	is deleted, and the new one is inserted into the bookset.  The
	bookset is then marked as EDITED. '''

	def __init__(self, bookset, index=None):
		self.bookset = bookset
		self.index = index
		self.setFocus = None
		if index <> None:
			self.tr = bookset[index]
		else:
			self.tr = None

		self.dateVar = StringVar()
		self.comVar  = StringVar()
		self.lines = []

		if self.tr:
			self.dateVar.set(string.split(self.tr.getDateString())[0])
			self.comVar.set(self.tr.comment)
			self.lines = map(self.makeLine, self.tr.lines)
			
		tkSimpleDialog.Dialog.__init__(self, Root, 'Edit Transaction')
		

	def makeLine(self, (account, amount, junk)=(None,None,None)):
		accountVar = StringVar()
		if account: accountVar.set(account)
		amountVar = DoubleVar()
		if amount: amountVar.set(amount)
		return (accountVar, amountVar, None, None)

	def addLine(self):
		try:
			i = self.map.index(self.focus_get()) + 1
		except:
			i = 0
		newLine = self.makeLine((None,None,None))
		self.lines[i:i] = [newLine]
		self.setFocus = i
		self.LayoutLines()

	def delLine(self):
		try:
			i = self.map.index(self.focus_get())
		except:
			return
		accountVar,amountVar,accountW,amountW = self.lines[i]
		del self.lines[i]
		accountW.grid_forget()
		amountW.grid_forget()
		self.LayoutLines()

	def body(self, master):

		master.config(relief=GROOVE, bd=4)

		if self.tr:
			l = Label(master, text='Transaction number: %d' % self.index)
			l.pack(side=TOP, pady=10)

		self.topGrid = Frame(master)
		self.topGrid.pack(side=TOP, padx=10, pady=10)
		self.topGrid.grid_columnconfigure(0, pad=20)
		
		Label(self.topGrid, text='Date').grid(col=0, row=0)
		Label(self.topGrid, text='Comment').grid(col=0, row=1)

		de = Entry(self.topGrid, textvariable=self.dateVar, width=11)
		de.grid(col=1, row=0, sticky='w')
		ce = Entry(self.topGrid, textvariable=self.comVar, width=45)
		ce.grid(col=1, row=1)

		self.dataGrid = Frame(master)
		self.dataGrid.pack(side=TOP, padx=10, pady=10)
		self.dataGrid.grid_rowconfigure(0, pad=20)
		
		Label(self.dataGrid, text='Account').grid(col=0, row=2)
		Label(self.dataGrid, text='Amount').grid(col=1, row=2)

		self.LayoutLines()
		
		buttons = Frame(master)
		buttons.pack(side=TOP, expand=YES, fill=X, pady=10)
		addB = Button(buttons, text='Add Line', command=self.addLine)
		addB.pack(side=LEFT, expand=YES)
		delB = Button(buttons, text='Delete Line', command=self.delLine)
		delB.pack(side=LEFT, expand=YES)

	def LayoutLines(self):
		self.map = []
		for i in range(len(self.lines)):
			accountVar, amountVar, accountW, amountW = self.lines[i]
			if not accountW:
				accountW = apply(OptionMenu, [self.dataGrid, accountVar] \
								+ self.bookset.getAccountList())
				accountW.configure(width=45)
			if not amountW:
				amountW = Entry(self.dataGrid, textvariable=amountVar,
								width=11)
			self.lines[i] = (accountVar, amountVar, accountW, amountW)

			accountW.grid(col=0, row=i+3)
			amountW.grid(col=1, row=i+3)
			self.map.append(amountW)
		if self.setFocus <> None:
			self.lines[self.setFocus][3].focus_set()
			self.setFocus = None

	def validate(self):
		try:
			asc2sec(self.dateVar.get())
		except:
			tkMessageBox.showerror('Error', 'Date string is invalid')
			return 0

		sum = 0
		for i in range(len(self.lines)):
			accountVar, amountVar, accountW, amountW = self.lines[i]
			if not accountVar.get():
				tkMessageBox.showerror('Error',
					'Account name in\nline %d is blank.'%(i+1))
				return 0

			try:
				value = amountVar.get()
			except:
				tkMessageBox.showerror('Error',
					'Amount in line %d\nis not a valid number.'%(i+1))
				return 0

			sum = sum + value

		if sum <> 0.0:
			tkMessageBox.showerror('Error',
				'The entries sum to %0.2f;\nSum must be zero.' % sum)
			return 0
			
		return 1

	def apply(self):
		transaction = Transaction()
		transaction.setDateString(self.dateVar.get())
		transaction.comment = self.comVar.get()
		for accountVar, amountVar, accountW, amountW in self.lines:
			transaction.addLine(accountVar.get(), amountVar.get())
		if self.index == None:
			self.bookset.add(transaction)
		else:
			self.bookset.edit(self.index, transaction)
		self.bookset.Changed()


######################################################################
## Main Application
######################################################################

def Main():
	if len(sys.argv) > 1:
		for file in sys.argv[1:]:
			JournalView(AugmentedBookset(file))
	else:
		JournalView()
	Root.mainloop()

if __name__ == '__main__':
	Main()
