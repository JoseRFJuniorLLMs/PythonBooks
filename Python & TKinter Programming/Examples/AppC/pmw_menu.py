from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('MenuBar')
Pmw.initialise()

balloon = Pmw.Balloon(root)

menuBar = Pmw.MenuBar(root, hull_relief=RAISED,	hull_borderwidth=1,
                      balloon=balloon)
menuBar.pack(fill=X)

menuBar.addmenu('Buttons', 'Simple Commands')
menuBar.addmenuitem('Buttons', 'command', 'Close this window',
                    font=('StingerLight', 14), label='Close')
menuBar.addmenuitem('Buttons', 'command',
                    bitmap="@bitmaps/RotateLeft", foreground='yellow')
menuBar.addmenuitem('Buttons', 'separator')
menuBar.addmenuitem('Buttons', 'command',
                    'Exit the application', label='Exit')

menuBar.addmenu('Cascade', 'Cascading Menus')
menuBar.addmenu('Checkbutton', 'Checkbutton Menus')
menuBar.addmenu('Radiobutton', 'Radiobutton Menus')

root.mainloop()

