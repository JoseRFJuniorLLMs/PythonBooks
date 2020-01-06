from Tkinter import *
import Pmw

class GUI:
    def __init__(self):
######################################################################
   	self.root = Tk()
        self.root.title('GUI Design 2')
        self.root.option_add('*Entry*background',     'lightblue')
        self.root.option_add('*font',   ('verdana', 10, 'bold'))
        
        Label(self.root, text='First Name').grid(row=0, sticky=W)
   	Pmw.EntryField(self.root, value='John').grid(row=0, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='Initial').grid(row=1, sticky=W)
        Pmw.EntryField(self.root, value='E').grid(row=1, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='Last Name').grid(row=2, sticky=W)
        Pmw.EntryField(self.root, value='Grayson').grid(row=2, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='Address 1').grid(row=3, sticky=W)
        Pmw.EntryField(self.root, value='My Street').grid(row=3, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='Address 2').grid(row=4, sticky=W)
        Pmw.EntryField(self.root, value='').grid(row=4, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='City').grid(row=5, sticky=W)
        Pmw.EntryField(self.root, value='My City').grid(row=5, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='State').grid(row=6, sticky=W)
        Pmw.EntryField(self.root, value='RI').grid(row=6, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='Zip').grid(row=7, sticky=W)
        Pmw.EntryField(self.root, value='01234').grid(row=7, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='Phone').grid(row=8, sticky=W)
        Pmw.EntryField(self.root, value='(401) 555-1212').grid(row=8, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='Position').grid(row=9, sticky=W)
        Pmw.EntryField(self.root, value='The Boss').grid(row=9, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='Employee #').grid(row=10, sticky=W)
        Pmw.EntryField(self.root, value='12345').grid(row=10, column=1,
                                                 padx=6, pady=2)
        Label(self.root, text='SS#').grid(row=11, sticky=W)
        Pmw.EntryField(self.root, value='123-45-6789').grid(row=11, column=1,
                                                 padx=6, pady=2)

        Button(self.root, text='OK',
               command=self.quit).grid(row=13, columnspan=2)

    def quit(self):
        import sys
        sys.exit()
        
myGUI = GUI()
myGUI.root.mainloop()

