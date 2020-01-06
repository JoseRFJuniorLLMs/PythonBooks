#! /usr/env/python

"""
WizardShell provides a GUI wizard framework.

WizardShell was derived from AppShell which was itself
derived from GuiAppD.py, originally created by
Doug Hellmann (doughellmann@mindspring.com).

"""

from Tkinter import *
import Pmw
import sys, string

class WizardShell(Pmw.MegaWidget):        
    wizversion      = '1.0'
    wizname         = 'Generic Wizard Frame'
    wizimage        = 'wizard.gif'
    
    frameWidth      = 467
    frameHeight     = 357
    padx            = 5
    pady            = 5
    panes           = 4
    
    busyCursor = 'watch'
    
    def __init__(self, **kw):
        optiondefs = (
            ('framewidth',     1,          Pmw.INITOPT),
            ('frameheight',    1,          Pmw.INITOPT))
        self.defineoptions(kw, optiondefs)
        
        self.root = Tk()
        self.initializeTk(self.root)
        Pmw.initialise(self.root)
        self.root.title(self.wizname)
        self.root.geometry('%dx%d' % (self.frameWidth, self.frameHeight))

        # Initialize the base class
        Pmw.MegaWidget.__init__(self, parent=self.root)
        
        # initialize the wizard
        self.wizardInit()

        # setup panes
        self.pCurrent = 0
        self.pFrame = [None] * self.panes
        
        # create the interface
        self.__createInterface()
        
        # create a table to hold the cursors for
        # widgets which get changed when we go busy
        self.preBusyCursors = None
        
        # pack the container and set focus
        # to ourselves
        self._hull.pack(side=TOP, fill=BOTH, expand=YES)
        self.focus_set()

        # initialize our options
        self.initialiseoptions(WizardShell)
        
    def wizardInit(self):
        # Called before interface is created (should be overridden).
        pass
        
    def initializeTk(self, root):
        # Initialize platform-specific options
        if sys.platform == 'mac':
            self.__initializeTk_mac(root)
        elif sys.platform == 'win32':
            self.__initializeTk_win32(root)
        else:
            self.__initializeTk_unix(root)

    def __initializeTk_colors_common(self, root):
        root.option_add('*background', 'grey')
        root.option_add('*foreground', 'black')
        root.option_add('*EntryField.Entry.background', 'white')
        root.option_add('*Entry.background', 'white')        
        root.option_add('*MessageBar.Entry.background', 'gray85')
        root.option_add('*Listbox*background', 'white')
        root.option_add('*Listbox*selectBackground', 'dark slate blue')
        root.option_add('*Listbox*selectForeground', 'white')
                        
    def __initializeTk_win32(self, root):
        self.__initializeTk_colors_common(root)
        root.option_add('*Font', 'Verdana 10 bold')
        root.option_add('*EntryField.Entry.Font', 'Courier 10')
        root.option_add('*Listbox*Font', 'Courier 10')
        
    def __initializeTk_mac(self, root):
        self.__initializeTk_colors_common(root)
        
    def __initializeTk_unix(self, root):
        self.__initializeTk_colors_common(root)

    def busyStart(self, newcursor=None):
        if not newcursor:
            newcursor = self.busyCursor
        newPreBusyCursors = {}
        for component in self.busyWidgets:
            newPreBusyCursors[component] = component['cursor']
            component.configure(cursor=newcursor)
            component.update_idletasks()
        self.preBusyCursors = (newPreBusyCursors, self.preBusyCursors)
        
    def busyEnd(self):
        if not self.preBusyCursors:
            return
        oldPreBusyCursors = self.preBusyCursors[0]
        self.preBusyCursors = self.preBusyCursors[1]
        for component in self.busyWidgets:
            try:
                component.configure(cursor=oldPreBusyCursors[component])
            except KeyError:
                pass
            component.update_idletasks()
              
    def __createWizardArea(self):
        # Create data area where data entry widgets are placed.
        self.__wizardArea = self.createcomponent('wizard',
                                                 (), None,
                                                 Frame,
                                                 (self._hull,), 
                                                 relief=FLAT, bd=1)
	self.__illustration = self.createcomponent('illust',
                                                   (), None,
                                                   Label,
                                                   (self.__wizardArea,)) 

        self.__illustration.pack(side=LEFT, expand=NO, padx=20)
        self.__wizimage = PhotoImage(file=self.wizimage)
        self.__illustration['image'] = self.__wizimage
        
	self.__dataArea = self.createcomponent('dataarea',
                                               (), None,
                                               Frame,
                                               (self.__wizardArea,), 
                                               relief=FLAT, bd=1)

        self.__dataArea.pack(side=LEFT, fill = 'both', expand = YES)
        self.__wizardArea.pack(side=TOP, fill=BOTH, expand=YES)

    def __createSeparator(self):
        self.__separator = self.createcomponent('separator',
                                                (), None,
                                                Frame,
                                                (self._hull,),
                                                relief=SUNKEN,
                                                bd=2, height=2)
        self.__separator.pack(fill=X, expand=YES)

    def __createCommandArea(self):
        # Create a command area for application-wide buttons.
        self.__commandFrame = self.createcomponent('commandframe',
                                                   (), None,
                                                   Frame,
                                                   (self._hull,),
                                                   relief=FLAT, bd=1)
        self.__commandFrame.pack(side=TOP, expand=NO, fill=X)

    def interior(self):
        # Retrieve the interior site where widgets should go.
        return self.__dataArea

    def changePicture(self, gif):
        if self.__wizimage: del self.__wizimage
        self.__wizimage = PhotoImage(file=gif)
        self.__illustration['image'] = self.__wizimage
        
    def buttonAdd(self, buttonName, command=None, state=1):
        # Add a button to the control area.
        frame = Frame(self.__commandFrame)
        newBtn = Button(frame, text=buttonName, command=command)
        newBtn.pack()
        newBtn['state'] = [DISABLED,NORMAL][state]
        frame.pack(side=RIGHT, ipadx=5, ipady=5)
        return newBtn

    def __createPanes(self):
        for i in range(self.panes):
            self.pFrame[i] = self.createcomponent('pframe',
                                               (), None,
                                               Frame,
                                               (self.interior(),),
                                               relief=FLAT, bd=1)
            if not i == self.pCurrent:
                self.pFrame[i].forget()
            else:
                self.pFrame[i].pack(fill=BOTH, expand=YES)

    def pInterior(self, idx):
        return self.pFrame[idx]

    def next(self):
        cpane = self.pCurrent
        self.pCurrent = self.pCurrent + 1
        self.prevB['state'] = NORMAL
        if self.pCurrent == self.panes - 1:
            self.nextB['text']    = 'Finish'
            self.nextB['command'] = self.done
        self.pFrame[cpane].forget()
        self.pFrame[self.pCurrent].pack(fill=BOTH, expand=YES)
       
    def prev(self):
        cpane = self.pCurrent
        self.pCurrent = self.pCurrent - 1
        if self.pCurrent <= 0:
            self.pCurrent = 0 
            self.prevB['state'] = DISABLED
        if cpane == self.panes - 1:
            self.nextB['text']    = 'Next'
            self.nextB['command'] = self.next
        self.pFrame[cpane].forget()
        self.pFrame[self.pCurrent].pack(fill=BOTH, expand=YES)

    def done(self):
        #to be Overridden
        pass

    def __createInterface(self):
        self.__createWizardArea()
        self.__createSeparator()
        self.__createCommandArea()
        self.__createPanes()
        #
        # Create the parts of the interface
        # which can be modified by subclasses
        #
        self.busyWidgets = ( self.root, )
        self.createInterface()

    def createInterface(self):
        # Override this method to create the interface for the wiz.
        pass
        
    def main(self):
        # This method should be left intact!
        self.pack()
        self.mainloop()
        
    def run(self):
        self.main()

class TestWizardShell(WizardShell):

        def createButtons(self):
            self.buttonAdd('Cancel',            command=self.quit, state=1) 
            self.nextB = self.buttonAdd('Next', command=self.next, state=1)
            self.prevB = self.buttonAdd('Prev', command=self.prev, state=0)
               
        def createMain(self):
            self.w1 = self.createcomponent('w1', (), None,
                                              Label,
                                              (self.pInterior(0),),
                                              text='Wizard Area 1')
            self.w1.pack()
            self.w2 = self.createcomponent('w2', (), None,
                                              Label,
                                              (self.pInterior(1),),
                                              text='Wizard Area 2')
            self.w2.pack()
                
        def createInterface(self):
            WizardShell.createInterface(self)
            self.createButtons()
            self.createMain()
        
        def done(self):
            print 'All Done'

if __name__ == '__main__':
        test = TestWizardShell()
        test.run()
