from Tkinter import *
import Pmw

positions = ('Janitor', 'Security Guard', 'Receptionist', 'Secretary',
             'Office Manager', 'Purchasing', 'Human Resources',
             'Engineer', 'Senior Engineer', 'Chief Engineer',
             'The Boss', 'The Owner')

class GUI:
    def __init__(self):
######################################################################
   	self.root = Tk()
        self.root.title('GUI Design 4')
        self.root.option_add('*Entry*background',     'lightblue')
        self.root.option_add('*font',   ('verdana', 10, 'bold'))
        
        self.f1=Frame(self.root, borderwidth=1)
        self.frx=Frame(self.f1, borderwidth=1)
        Label(self.frx, text='Name', width=10, anchor=W).pack(side=LEFT, expand=NO, fill=BOTH)
   	Pmw.EntryField(self.frx, value='John', entry_width=12).pack(side=LEFT, expand=NO, fill=BOTH)
        Pmw.EntryField(self.frx, value='E', entry_width=1).pack(side=LEFT, expand=NO, fill=BOTH, padx=4)
        Pmw.EntryField(self.frx, value='Grayson', entry_width=20).pack(side=RIGHT, expand=YES, fill=BOTH)
        self.frx.pack(side=TOP, expand=YES, fill=BOTH, padx=8, pady=1)
        self.f1.pack(side=TOP, expand=YES, fill=BOTH, padx=8, pady=1)

        self.f2=Frame(self.root, borderwidth=1)
        self.frc=Frame(self.f2, borderwidth=1)
        Label(self.frc, text='Position', width=10, anchor=W).pack(side=LEFT, expand=NO)
	self.combobox = Pmw.ComboBox(self.frc, scrolledlist_items = positions)
	self.combobox.pack(side=LEFT, fill=BOTH, expand=NO)
	self.combobox.selectitem(positions[10])
        Pmw.EntryField(self.frc, value='12345', entry_width=7).pack(side=RIGHT, expand=NO, fill=BOTH)
        Label(self.frc, text='Employee #').pack(side=RIGHT, expand=NO, fill=BOTH)
        self.frc.pack(side=TOP, expand=YES, fill=BOTH, padx=8, pady=1)
        self.frd=Frame(self.f2, borderwidth=1)
        Label(self.frd, text='Phone     ', width=10, anchor=W).pack(side=LEFT, expand=NO, fill=BOTH)
        Label(self.frd, text='(', anchor=W).pack(side=LEFT, expand=NO, fill=BOTH)
        Pmw.EntryField(self.frd, value='401', entry_width=3).pack(side=LEFT, expand=NO, fill=BOTH)
        Label(self.frd, text=') ', anchor=W).pack(side=LEFT, expand=NO, fill=BOTH)
        Pmw.EntryField(self.frd, value='555', entry_width=3).pack(side=LEFT, expand=NO, fill=BOTH)
        Label(self.frd, text='-', anchor=W).pack(side=LEFT, expand=NO, fill=BOTH)
        Pmw.EntryField(self.frd, value='1212',entry_width=4).pack(side=LEFT, expand=NO, fill=BOTH)
        Pmw.EntryField(self.frd, value='6789', entry_width=4).pack(side=RIGHT, expand=NO, fill=Y)
        Label(self.frd, text='-', anchor=E).pack(side=RIGHT, expand=NO, fill=BOTH)
        Pmw.EntryField(self.frd, value='45', entry_width=2).pack(side=RIGHT, expand=NO, fill=BOTH)
        Label(self.frd, text='-', anchor=E).pack(side=RIGHT, expand=NO, fill=BOTH)
        Pmw.EntryField(self.frd, value='123', entry_width=3).pack(side=RIGHT, expand=NO, fill=BOTH)
        Label(self.frd, text='SS#').pack(side=RIGHT, expand=NO, fill=BOTH)
        self.frd.pack(side=TOP, expand=YES, fill=BOTH, padx=8, pady=1)
        self.f2.pack(side=TOP, expand=YES, fill=BOTH, padx=8, pady=1)
        
        self.f3=Frame(self.root, borderwidth=1)
        self.f4=Frame(self.f3, borderwidth=1)
        Label(self.f4, text='Address 1  ', width=10, anchor=W).pack(side=LEFT, expand=NO, fill=BOTH)
        Pmw.EntryField(self.f4, value='My Street', entry_width=20).pack(side=RIGHT, expand=YES, fill=BOTH)
        self.f4.pack(side=TOP, expand=YES, fill=BOTH, padx=8, pady=1)
        self.f5=Frame(self.f3, borderwidth=1)
        Label(self.f5, text='Address 2  ', width=10, anchor=W).pack(side=LEFT, expand=NO, fill=BOTH)
        Pmw.EntryField(self.f5, value='', entry_width=20).pack(side=RIGHT, expand=YES, fill=BOTH)
        self.f5.pack(side=TOP, expand=YES, fill=BOTH, padx=8, pady=1)
        self.f6=Frame(self.f3, borderwidth=1)
        Label(self.f6, text='City       ', width=10, anchor=W).pack(side=LEFT, expand=NO, fill=BOTH)
        Pmw.EntryField(self.f6, value='My City', entry_width=16).pack(side=LEFT, expand=YES, fill=BOTH)
        Label(self.f6, text='State').pack(side=LEFT, expand=NO, fill=BOTH, padx=2)
        Pmw.EntryField(self.f6, value='RI', entry_width=2).pack(side=LEFT, expand=NO, fill=BOTH)
        Label(self.f6, text='Zip').pack(side=LEFT, expand=NO, fill=BOTH, padx=2)
        Pmw.EntryField(self.f6, value='01234', entry_width=9).pack(side=LEFT, expand=NO, fill=BOTH)
        self.f6.pack(side=TOP, expand=YES, fill=BOTH, padx=8, pady=1)
        self.f3.pack(side=TOP, expand=YES, fill=BOTH, padx=8, pady=1)
        self.f7=Frame(self.root, borderwidth=1)
        Button(self.f7, text='OK', command=self.quit).pack(expand=NO, fill=Y)
        self.f7.pack(side=TOP, expand=YES, fill=BOTH, padx=8, pady=1)
        
    def quit(self):
        import sys
        sys.exit()
        
myGUI = GUI()
myGUI.root.mainloop()

