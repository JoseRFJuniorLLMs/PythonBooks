from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('Notebook')
Pmw.initialise()

nb = Pmw.NoteBook(root)
p1 = nb.add('Page 1')
p2 = nb.add('Page 2')
p3 = nb.add('Page 3')

nb.pack(padx=5, pady=5, fill=BOTH, expand=1)

Button(p1, text='This is text on page 1', fg='blue').pack(pady=40)
c = Canvas(p2, bg='gray30')
w = c.winfo_reqwidth()
h = c.winfo_reqheight()
c.create_oval(10,10,w-10,h-10,fill='DeepSkyBlue1')
c.create_text(w/2,h/2,text='This is text on a canvas', fill='white',
	    font=('Verdana', 14, 'bold'))
c.pack(fill=BOTH, expand=1) 

nb.setnaturalpagesize()

root.mainloop()

