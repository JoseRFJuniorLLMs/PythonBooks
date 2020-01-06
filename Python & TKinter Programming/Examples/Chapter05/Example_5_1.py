from Tkinter import *

class App:
    def __init__(self, master):
        Button(master, text='Left').pack(side=LEFT)
        Button(master, text='Center').pack(side=LEFT)
        Button(master, text='Right').pack(side=LEFT)        

root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 1")
display = App(root)
root.mainloop()
