#! /bin/env/python

from Tkinter      import *
from Components_1 import *
from GUICommon    import *
from Common       import *

class Router(Frame):
    def __init__(self, master=None):
	Frame.__init__(self, master)
	Pack.config(self)
	self.createChassis()

    def createChassis(self):
	self.chassis = Chassis(self)
        # Realize the outer frame (which
        # was forgotten when created)          [1]
	self.chassis.outer.pack(expand=0)   

if __name__ == '__main__':
    root = Router()
    root.master.title("CisForTron")
    root.master.iconname("CisForTron")
    root.mainloop()
            
