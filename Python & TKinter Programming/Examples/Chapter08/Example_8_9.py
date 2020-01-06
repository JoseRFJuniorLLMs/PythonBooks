from   Tkinter import *
import Pmw
import os
import AppShell
from   datadictionary2 import *

class DDNotebook(AppShell.AppShell):
    usecommandarea = 1
    appname        = 'Update Crew Information'        
    dictionary     = 'crewmembers'
    frameWidth     = 435
    frameHeight    = 520
    
    def createButtons(self):
        self.buttonAdd('Save',
              helpMessage='Save current data',
              statusMessage='Write current information to database',
              command=self.save)
        self.buttonAdd('Close',
              helpMessage='Close Screen',
              statusMessage='Exit',
               command=self.close)
        
    def createNotebook(self):
        self.notebook = self.createcomponent('notebook', (), None,
                                         Pmw.NoteBookR, (self.interior(),),)
        self.notebook.pack(side=TOP, expand=YES, fill=BOTH, padx=5, pady=5)
        self.formwidth = self.root.winfo_width()
        
    def addPage(self, dictionary):
        table, top, anchor, incr, fields, \
	    title, keylist = dataDict[dictionary]
	self.notebook.add(table, label=title)
        self.current = 0
        ypos = top
	idx = 0
        for label, field, width, proc, valid, nonblank in fields:
            pstr = 'Label(self.notebook.page(table).interior(),'\
                   'text="%s").place(relx=%f,rely=%f, anchor=E)\n' % \
                   (label, (anchor-0.02), ypos)
            if idx == keylist[0]:
                pstr = '%sself.%s=Entry(self.notebook.page(table).interior(),'\
                       'text="",insertbackground="yellow", width=%d+1,'\
                       'highlightthickness=1)\n' % (pstr,field,width)
            else:
                pstr = '%sself.%s=Entry(self.notebook.page(table).interior(),'\
                       'text="", insertbackground="yellow",'\
                       'width=%d+1)\n' % (pstr,field,width)
	    pstr = '%sself.%s.place(relx=%f, rely=%f,'\
                   'anchor=W)\n' % (pstr,field,(anchor+0.02),ypos)
	    exec '%sself.%sV=StringVar()\n'\
                 'self.%s["textvariable"] = self.%sV' % \
                                          (pstr,field,field,field)
	    ypos = ypos + incr
	    idx = idx + 1

    def createPages(self):
        self.addPage('general')
        self.addPage('language')
        self.addPage('crewqualifications')

        self.update_display()

    def update_display(self):
        pass
    
    def save(self):
        pass
    def close(self):
        self.quit()

    def createInterface(self):
        AppShell.AppShell.createInterface(self)
        self.createButtons()
        self.createNotebook()
        self.createPages()
        
if __name__ == '__main__':
    ddnotebook = DDNotebook()
    ddnotebook.run()
