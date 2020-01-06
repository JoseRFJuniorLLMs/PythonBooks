import string
from Tkinter import *
from validation import *

class EntryFormatting:
    def __init__(self, master):
        frame = Frame(master)
        Label(frame, text='   ').grid(row=0, column=0,sticky=W)
        Label(frame, text='   ').grid(row=0, column=3,sticky=W)

        self._ipaddr = self.createField(frame, width=16, row=0, col=2,
                             label='Phone Number:\n(nnn)-nnn-nnn',
                             format=self.fmtPhone, enter=self.activate)
        self._crdprt = self.createField(frame, width=11, row=1, col=2,
                 label='SSN#:', format=self.fmtSSN, enter=self.activate)

        frame.pack(side=TOP, padx=15, pady=15)
        
    def createField(self, master, label='', text='', width=1,
                    format=None, enter=None, row=0, col=0):
        Label(master, text=label).grid(row=row, column=col-1,
                                       padx=15, sticky=W)
        id = Entry(master, text=text, width=width, takefocus=1)
        id.bind('<KeyRelease>', format)
        id.bind('<Return>',   enter)
        id.grid(row=row, column=col, pady=10, sticky=W)
        return id
    
    def activate(self, event):
        print '<Return>: value is', event.widget.get()

    def fmtPhone(self, event):
        current = event.widget.get()
        if len(current) == 1:
            if event.char in '0123456789':
                current = '1-(%s' % current
            else:
                event.widget.bell()
                current = ''
        elif len(current) == 6:
            current = '%s)-' % current
        elif len(current) == 11:
            current = '%s-' % current
        event.widget.delete(0, END)
        event.widget.insert(0, current)

    def fmtSSN(self, event):
        current = event.widget.get()
        if len(current) in [3, 6]:
            current = '%s-' % current
        event.widget.delete(0, END)
        event.widget.insert(0, current)

######################################################################

root = Tk()
root.option_add('*Font', 'Verdana 10 bold')
root.option_add('*Entry.Font', 'Courier 10')
root.title('Entry  Formatting')

top = EntryFormatting(root)
quit = Button(root, text='Quit', command=root.destroy)
quit.pack(side = 'bottom')
 
root.mainloop()
