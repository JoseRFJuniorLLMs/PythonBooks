from Tkinter import *

class App:
    def __init__(self, master):
        fm = Frame(master)
        Button(fm, text='Top').pack(side=TOP)
        Button(fm, text='This is the Center button').pack(side=TOP)
        Button(fm, text='Bottom').pack(side=TOP)        
        fm.pack()

root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 2a")
display = App(root)
root.mainloop()
