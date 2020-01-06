from Tkinter import *

class App:
    def __init__(self, master):
        master.geometry("300x200")
        fm = Frame(master)
        Button(fm, text='Left').pack(side=LEFT, expand=YES)
        Button(fm, text='Center').pack(side=LEFT, expand=YES)
        Button(fm, text='Right').pack(side=LEFT, expand=YES)
        fm.pack(fill=BOTH, expand=YES)

        
root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 6")
display = App(root)
root.mainloop()
