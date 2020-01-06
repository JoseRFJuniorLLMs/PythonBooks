from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('Notebook S')
Pmw.initialise()

nb = Pmw.NoteBookS(root)
nb.addPage('Page 1')
nb.addPage('Page 2')
nb.addPage('Page 3')

f1 = nb.getPage('Page 1')
f2 = nb.getPage('Page 2')
f3 = nb.getPage('Page 3')

nb.pack(pady=10, padx=10, fill=BOTH, expand=1)

Button(f1, text='This is text on page 1', fg='blue').pack(pady=40)
c = Canvas(f2, bg='gray30')
w = c.winfo_reqwidth()
h = c.winfo_reqheight()
c.create_oval(10,10,w-10,h-10,fill='DeepSkyBlue1')
c.create_text(w/2,h/2,text='This is text on a canvas', fill='white',
	    font=('Verdana', 14, 'bold'))
c.pack(fill=BOTH, expand=1) 

root.mainloop()

