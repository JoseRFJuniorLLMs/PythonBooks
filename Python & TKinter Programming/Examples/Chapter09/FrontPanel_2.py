#! /bin/env/python

from Tkinter      import *
from Components_2 import *
from GUICommon    import *
from Common       import *

class Router(Frame):
    def __init__(self, master=None):
	Frame.__init__(self, master)
	Pack.config(self)
	self.createChassis()

    def createChassis(self):
	self.chassis = Chassis(self)
	self.chassis.outer.pack(expand=0)   # This realizes the chassis

if __name__ == '__main__':
    root = Router()
    root.master.title("CisForTron")
    root.master.iconname("CisForTron")
    root.mainloop()
            
