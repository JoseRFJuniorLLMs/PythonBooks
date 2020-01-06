from   Tkinter import *
import Pmw
import os
import AppShell
from   datadictionary import *

class DDForm(AppShell.AppShell):
    usecommandarea = 1
    appname        = 'Update Crew Information'        
    dictionary     = 'crewmembers'
    frameWidth     = 600
    frameHeight    = 590
    
    def createButtons(self):
        self.buttonAdd('Save',
              helpMessage='Save current data',
              statusMessage='Write current information to database',
              command=self.save)
        self.buttonAdd('Undo',
              helpMessage='Ignore changes',
              statusMessage='Do not save changes to database',
              command=self.undo)
        self.buttonAdd('New',
              helpMessage='Create a New record',
              statusMessage='Create New record',
              command=self.new)
        self.buttonAdd('Delete',
              helpMessage='Delete current record',
              statusMessage='Delete this record',
              command=self.delete)
        self.buttonAdd('Print',
              helpMessage='Print this screen',
              statusMessage='Print data in this screen',
              command=self.printme)
        self.buttonAdd('Prev',
              helpMessage='Previous record',
              statusMessage='Display previous record',
              command=self.prev)
        self.buttonAdd('Next',
              helpMessage='Next record',
              statusMessage='Display next record',
              command=self.next)
        self.buttonAdd('Close',
              helpMessage='Close Screen',
              statusMessage='Exit',
               command=self.close)
        
    def createForm(self):
        self.form = self.createcomponent('form', (), None,
                                         Frame, (self.interior(),),)
        self.form.pack(side=TOP, expand=YES, fill=BOTH)
        self.formwidth = self.root.winfo_width()
        
    def createFields(self):
        self.table, self.top, self.anchor, self.incr, self.fields, \
	    self.title, self.keylist = dataDict[self.dictionary]

        self.records    = []
	self.dirty      = FALSE
	self.changed    = []
        self.newrecs    = []
        self.deleted    = []
	self.checkDupes = FALSE
        self.delkeys    = []
 
        self.ypos = self.top

        self.recrows = len(self.records)

        if self.recrows < 1:     # Create one!
            self.recrows = 1
            trec = []
            for i in range(len(self.fields)):
                trec.append(None)
            self.records.append((trec))
            
        Label(self.form, text=self.title, width=self.formwidth-4,
              bd=0).place(relx=0.5, rely=0.025, anchor=CENTER)
####################################################################

        self.lmarker = Label(self.form, text="", bd=0, width=10)
        self.lmarker.place(relx=0.02, rely=0.99, anchor=SW)
        self.rmarker = Label(self.form, text="", bd=0, width=10)
        self.rmarker.place(relx=0.99, rely=0.99, anchor=SE)

        self.current = 0
	idx = 0
        for label, field, width, proc, valid, nonblank in self.fields:
            pstr = 'Label(self.form,text="%s").place(relx=%f,rely=%f,'\
                   'anchor=E)\n' % (label, (self.anchor-0.02), self.ypos)
            if idx == self.keylist[0]:
                pstr = '%sself.%s=Entry(self.form,text="",'\
                       'insertbackground="yellow", width=%d+1,'\
                       'highlightthickness=1)\n' % (pstr,field,width)
            else:
                pstr = '%sself.%s=Entry(self.form,text="",'\
                       'insertbackground="yellow",'\
                       'width=%d+1)\n' % (pstr,field,width)
	    pstr = '%sself.%s.place(relx=%f, rely=%f,'\
                   'anchor=W)\n' % (pstr,field,(self.anchor+0.02),self.ypos)
	    exec '%sself.%sV=StringVar()\n'\
                 'self.%s["textvariable"] = self.%sV' % \
                                          (pstr,field,field,field)
	    self.ypos = self.ypos + self.incr
	    idx = idx + 1

        self.update_display()

    def update_display(self):
	idx = 0
        for label, field, width, proc, valid, nonblank in self.fields:
            v=self.records[self.current][idx]
            if not v:v=""
            exec 'self.%sV.set(v)' % field
	    idx = idx + 1
        if self.current in self.deleted:
            self.rmarker['text'] = 'Deleted'
        elif self.current in self.newrecs:
            self.rmarker['text'] = 'New'
        else:
            self.rmarker['text'] = ''
        if self.dirty:
	    self.lmarker['text']       = "Modified"
	    self.lmarker['foreground'] = "#FF3333"
	else:
	    self.lmarker['text']       = ""
	    self.lmarker['foreground'] = "#00FF44"

        # We'll set focus on the first widget
        label, field, width, proc, valid, nonblank = self.fields[0]
        exec 'self.%s.focus_set()' % field
            
    def update_display(self):
	idx = 0
        for label, field, width, proc, valid, nonblank in self.fields:
            v=self.records[self.current][idx]
            if not v:v=""
            exec 'self.%sV.set(v)' % field
	    idx = idx + 1
        if self.current in self.deleted:
            self.rmarker['text'] = 'Deleted'
        elif self.current in self.newrecs:
            self.rmarker['text'] = 'New'
        else:
            self.rmarker['text'] = ''
        if self.dirty:
	    self.lmarker['text']       = "Modified"
	    self.lmarker['foreground'] = "#FF3333"
	else:
	    self.lmarker['text']       = ""
	    self.lmarker['foreground'] = "#00FF44"

        label, field, width, proc, valid, nonblank = self.fields[0]
        exec 'self.%s.focus_set()' % field
            
    def save(self):
        pass
    def next(self):
        pass
    def prev(self):
        pass
    def delete(self):
        pass
    def clear(self):
        pass
    def undo (self):
        pass
    def new(self):
        pass
    def printme(self):
        pass
    def close(self):
        pass

    def createInterface(self):
        AppShell.AppShell.createInterface(self)
        self.createButtons()
        self.createForm()
        self.createFields()
        
if __name__ == '__main__':
    ddform = DDForm()
    ddform.run()



