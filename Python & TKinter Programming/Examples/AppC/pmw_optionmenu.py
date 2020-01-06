from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('OptionMenu')
Pmw.initialise()

var = StringVar()
var.set('Quantity Surveyor')
opt_menu = Pmw.OptionMenu(root, labelpos=W,
        label_text='Choose profession:', menubutton_textvariable=var,
        items=('Stockbroker', 'Quantity Surveyor', 'Church Warden', 'BRM'),
	menubutton_width=16)
opt_menu.pack(anchor=W, padx=20, pady=30)

root.mainloop()

