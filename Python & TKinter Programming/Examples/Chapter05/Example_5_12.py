from Tkinter import *

class App:
    def __init__(self, master):
        fm = Frame(master)
        Button(fm, text='Top').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='Center').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='Bottom').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='Left').pack(side=LEFT)
        Button(fm, text='This is the Center button').pack(side=LEFT)
        Button(fm, text='Right').pack(side=LEFT)        
        fm.pack(fill=BOTH, expand=YES)
        
root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 12")
display = App(root)
root.mainloop()
