from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('PanedWidget')
Pmw.initialise()

pane = Pmw.PanedWidget(root, hull_width=400, hull_height=300)
pane.add('top', min=100)
pane.add('bottom', min=100)

topPane = Pmw.PanedWidget(pane.pane('top'), orient=HORIZONTAL)
for num in range(4):
    if num == 1:
        name = 'Fixed\nSize'
        topPane.add(name, min=.2, max=.2)
    else:
        name = 'Pane\n' + str(num)
        topPane.add(name, min=.1, size=.25)
    button = Button(topPane.pane(name), text=name)
    button.pack(expand=1)

topPane.pack(expand=1, fill=BOTH)
pane.pack(expand=1, fill=BOTH)

root.mainloop()

