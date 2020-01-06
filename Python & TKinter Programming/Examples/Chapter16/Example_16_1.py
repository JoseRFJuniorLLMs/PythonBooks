from Tkinter import *
import Pmw

class GUI:
    def __init__(self):
######################################################################
   	self.root = Tk()
        self.root.title('GUI Design 1')
        self.root.option_add('*font',   ('courier', 8))
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='First Name',
                       value='John').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='Initial',
                       value='E').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='Last Name',
                       value='Grayson').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='Address 1',
                       value='My Street').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='Address 2',
                       value='').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='City',
                       value='My City').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='State',
                       value='RI').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='Zip',
                       value='01234').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='Phone',
                       value='(401) 555-1212').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='Position',
                       value='The Boss').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='Employee #',
                       value='12345').pack(side=TOP, expand=YES, fill=BOTH)
        Pmw.EntryField(self.root, labelpos = 'w',
                       label_text='SS#',
                       value='123-45-6789').pack(side=TOP, expand=YES, fill=BOTH)

        Button(self.root, text='OK', command=self.quit).pack(side=TOP)

    def quit(self):
        import sys
        sys.exit()
        
myGUI = GUI()
myGUI.root.mainloop()

