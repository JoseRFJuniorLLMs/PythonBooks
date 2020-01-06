from Tkinter import *

class App:
    def __init__(self, master):
        master.geometry("300x200")
        fm = Frame(master)
        Button(fm, text='Top').pack(side=TOP, fill=X)
        Button(fm, text='Center').pack(side=TOP, fill=X)
        Button(fm, text='Bottom').pack(side=TOP, fill=X)
        fm.pack(fill=BOTH, expand=YES)

        
root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 7a")
display = App(root)
root.mainloop()
