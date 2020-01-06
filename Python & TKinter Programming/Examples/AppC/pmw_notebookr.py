from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('Notebook R')
Pmw.initialise()

nb = Pmw.NoteBookR(root)
nb.add('p1', label='Page 1')
nb.add('p2', label='Page 2')
nb.add('p3', label='Page 3')

p1 = nb.page('p1').interior()
p2 = nb.page('p2').interior()
p3 = nb.page('p3').interior()

nb.pack(padx=5, pady=5, fill=BOTH, expand=1)

Button(p1, text='This is text on page 1', fg='blue').pack(pady=40)
c = Canvas(p2, bg='gray30')
w = c.winfo_reqwidth()
h = c.winfo_reqheight()
c.create_oval(10,10,w-10,h-10,fill='DeepSkyBlue1')
c.create_text(w/2,h/2,text='This is text on a canvas', fill='white',
	    font=('Verdana', 14, 'bold'))
c.pack(fill=BOTH, expand=1) 

root.mainloop()

