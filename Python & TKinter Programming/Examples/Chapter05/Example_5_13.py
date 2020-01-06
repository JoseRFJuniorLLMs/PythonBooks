from Tkinter import *

class App:
    def __init__(self, master):
        fm = Frame(master)
        Button(fm, text='Top').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='Center').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='Bottom').pack(side=TOP, anchor=W, fill=X, expand=YES)
        fm.pack(side=LEFT, fill=BOTH, expand=YES)
        fm2 = Frame(master)
        Button(fm2, text='Left').pack(side=LEFT)
        Button(fm2, text='This is the Center button').pack(side=LEFT)
        Button(fm2, text='Right').pack(side=LEFT)        
        fm2.pack(side=LEFT, padx=10)
        
root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 13")
display = App(root)
root.mainloop()
