from Tkinter import *
from tkSimpleDialog import Dialog
import Pmw

class MixedWidgets(Dialog):

    def body(self, master):
        Label(master, text='Select Case:').grid(row=0, sticky=W)
        Label(master, text='Select Type:').grid(row=1, sticky=W)
        Label(master, text='Enter Value:').grid(row=2, sticky=W)

        self.combo1 = Pmw.ComboBox(master,
                                   scrolledlist_items=("Upper","Lower","Mixed"),
                                   entry_width=12, entry_state="disabled",
                                   selectioncommand = self.ripple)
	self.combo1.selectitem("Upper")
        self.combo1.component('entry').config(background='gray80')

        self.combo2 = Pmw.ComboBox(master, scrolledlist_items=(),
                                   entry_width=12, entry_state="disabled")
        self.combo2.component('entry').config(background='gray80')
        
        self.entry1  = Entry(master, width = 12)

        self.combo1.grid(row=0, column=1, sticky=W)
        self.combo2.grid(row=1, column=1, sticky=W)
        self.entry1.grid(row=2, column=1, sticky=W)

        return self.combo1

    def apply(self):
        c1 = self.combo1.get()
        c2 = self.combo2.get()        
        e1 = self.entry1.get()
        print c1, c2, e1

    def ripple(self, value):
        lookup = {'Upper': ("ANIMAL", "VEGETABLE", "MINERAL"),
                  'Lower': ("animal", "vegetable", "mineral"),
                  'Mixed': ("Animal", "Vegetable", "Mineral")}

        items = lookup[value]
        self.combo2.setlist(items)
	self.combo2.selectitem(items[0])

root = Tk()
dialog = MixedWidgets(root)
