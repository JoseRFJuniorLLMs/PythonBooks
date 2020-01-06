from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('ScrolledFrame')
Pmw.initialise()

global row, col
row = col = 0
sf = frame = None

def addButton():
    global row, col
    button = Button(frame, text = '(%d,%d)' % (col, row))
    button.grid(row=row, col=col, sticky='nsew')

    frame.grid_rowconfigure(row, weight=1)
    frame.grid_columnconfigure(col, weight=1)
    sf.reposition()

    if col == row:
        col = 0
        row = row + 1
    else:
        col = col + 1

sf = Pmw.ScrolledFrame(root, labelpos=N, label_text='ScrolledFrame',
		usehullsize=1, hull_width=400, hull_height=220)

sf.pack(padx=5, pady=3, fill='both', expand=1)
frame = sf.interior()

for i in range(250):
    addButton()

root.mainloop()



