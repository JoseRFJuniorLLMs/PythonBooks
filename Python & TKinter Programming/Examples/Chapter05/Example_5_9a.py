from Tkinter import *

class App:
    def __init__(self, master):
        master.geometry("300x200")
        fm = Frame(master)
        Button(fm, text='Top').pack(side=TOP, fill=BOTH, expand=1)
        Button(fm, text='Center').pack(side=TOP, fill=BOTH, expand=1)
        Button(fm, text='Bottom').pack(side=TOP, fill=BOTH, expand=1)
        fm.pack(fill=BOTH, expand=YES)

        
root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 9a")
display = App(root)
root.mainloop()
