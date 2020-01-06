#! /bin/env/python

from Tkinter      import *
from Components_4 import *
from GUICommon    import *
from Common       import *

class EC6110(Frame):
    def __init__(self, master=None):
	Frame.__init__(self, master)
	Pack.config(self)
	self.createChassis()

    def createChassis(self):
	self.chassis = C6C110_Chassis(self)
	self.chassis.outer.pack(expand=0)   # This realizes the chassis

if __name__ == '__main__':
    root = EC6110()
    root.master.title("EC6110")
    root.master.iconname("EC6110")
    root.mainloop()
            
