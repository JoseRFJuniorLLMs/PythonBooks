from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('LabeledWidget')
Pmw.initialise()

frame = Frame(root, background = 'gray80')
frame.pack(fill=BOTH, expand=1)

lw = Pmw.LabeledWidget(frame, labelpos='n', label_text='Sunset on Cat Island')
lw.component('hull').configure(relief=SUNKEN, borderwidth=3)
lw.pack(padx=10, pady=10)
img = PhotoImage(file='chairs.gif')
cw = Button(lw.interior(), background='yellow', image=img)
cw.pack(padx=10, pady=10, expand=1, fill=BOTH)

root.mainloop()

