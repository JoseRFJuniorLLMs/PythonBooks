from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('Group')
Pmw.initialise()

w = Pmw.Group(root, tag_text='place label here')
w.pack(fill=BOTH, expand=1, padx=6, pady=6)
cw = Label(w.interior(), text='A group with a\nsimple Label tag')
cw.pack(padx=2, pady=2, expand=1, fill=BOTH)

w = Pmw.Group(root, tag_pyclass=None)
w.pack(fill=BOTH, expand=1, padx=6, pady=6)
cw = Label(w.interior(), text='A group\nwithout a tag')
cw.pack(padx=2, pady=2, expand=1, fill=BOTH)

w = Pmw.Group(root, tag_pyclass=Checkbutton,
              tag_text='checkbutton', tag_foreground='blue')
w.pack(fill=BOTH, expand=1, padx=6, pady=6)
cw = Frame(w.interior(),width=150,height=20)
cw.pack(padx=2, pady=2, expand=1, fill=BOTH)

root.mainloop()

