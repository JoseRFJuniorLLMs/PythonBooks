from Tkinter import *

class App:
    def __init__(self, master):
        fm = Frame(master)
        Button(fm, text='Left').pack(side=TOP)
        Button(fm, text='Center').pack(side=LEFT)
        Button(fm, text='Right').pack(side=LEFT)        
        fm.pack()

root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 3")
display = App(root)
root.mainloop()
