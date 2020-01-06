from Tkinter import *

class App:
    def __init__(self, master):
        fm = Frame(master, width=300, height=200)
        Button(fm, text='Left').pack(side=LEFT)
        Button(fm, text='Center').pack(side=LEFT)
        Button(fm, text='Right').pack(side=LEFT)        
        fm.pack()

root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 4")
display = App(root)
root.mainloop()
