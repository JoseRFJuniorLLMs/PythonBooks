#! /usr/env/python

from Tkinter import *
import Pmw
import sys, string

import WizardShell

class Installer(WizardShell.WizardShell):
    wizname = 'Install Widgets'
    panes   = 4

    def createButtons(self):
        self.buttonAdd('Cancel',            command=self.quit, state=1) 
        self.nextB = self.buttonAdd('Next', command=self.next, state=1)
        self.prevB = self.buttonAdd('Prev', command=self.prev, state=0)
               
    def createTitle(self, idx, title):
        label = self.createcomponent('l%d' % idx, (), None,
                                Label,(self.pInterior(idx),),
                                text=title,
                                font=('verdana', 18, 'bold', 'italic'))
        label.pack()
        return label
    
    def createExplanation(self, idx):
        text = self.createcomponent('t%d' % idx, (), None,
                                    Text,(self.pInterior(idx),),
                                    bd=0, wrap=WORD, height=6)
        fd = open('install%d.txt' % (idx+1))
        text.insert(END, fd.read())
        fd.close()
        text.pack(pady=15)
            
    def createPanelOne(self):
        self.createTitle(0, 'Welcome!')
        self.createExplanation(0)

    def createPanelTwo(self):
        self.createTitle(1, 'Select Destination\nDirectory')
        self.createExplanation(1)
        frame = Frame(self.pInterior(1), bd=2, relief=GROOVE)
        self.entry = Label(frame, text='C:\\Widgets\\WidgetStorage',
                           font=('Verdana', 10))
        self.entry.pack(side=LEFT, padx=10)
        self.btn   = Button(frame, text='Browse...')
        self.btn.pack(side=LEFT, ipadx=5, padx=5, pady=5)
        frame.pack()
            
    def createPanelThree(self):
        self.createTitle(2, 'Select Components')
        self.createExplanation(2)
        frame = Frame(self.pInterior(2), bd=0)
        idx = 0
        for label, size in [('Monkey','526k'),('Aardvark','356k'),
                            ('Warthog','625k'),
                            ('Reticulated Python','432k')]:
            ck  = Checkbutton(frame).grid(row=idx, column=0)
            lbl = Label(frame, text=label).grid(row=idx, column=1,
                                                columnspan=4, sticky=W)
            siz = Label(frame, text=size).grid(row=idx, column=5)
            idx = idx + 1
        frame.pack()
            
    def createPanelFour(self):
        self.createTitle(3, 'Finish Installation')
        self.createExplanation(3)

    def createInterface(self):
        WizardShell.WizardShell.createInterface(self)
        self.createButtons()
        self.createPanelOne()
        self.createPanelTwo()
        self.createPanelThree()
        self.createPanelFour()
        
    def done(self):
        print 'This is where the work starts!'

if __name__ == '__main__':
    install = Installer()
    install.run()
