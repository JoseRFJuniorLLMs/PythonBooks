from Tkinter import *

class App:
    def __init__(self, master):
        master.geometry("300x200")
        fm = Frame(master)
        Button(fm, text='side=TOP, anchor=NW').pack(side=TOP, anchor=NW, expand=YES)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='side=TOP, anchor=E').pack(side=TOP, anchor=E, expand=YES)
        fm.pack(fill=BOTH, expand=YES)

        
root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 11")
display = App(root)
root.mainloop()
