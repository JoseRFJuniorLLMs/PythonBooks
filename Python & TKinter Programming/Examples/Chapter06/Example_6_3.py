from Tkinter import *

def displayHelp(event):
    print 'hlp', event.keysym
    
def sayKey(event):
    print 'say',event.keysym, event.char
    
def printWindow(event):
    print 'prt', event.keysym
    
def cursor(*args):
    print 'cursor'

def unbindThem(*args):
    print 'Gone...'
    root.unbind_all('<F1>')
    root.unbind_class('Entry', '<KeyPress>')
    root.unbind('<Alt_L>')
    root.unbind('<Control-Shift-Down>')

root = Tk()

frame = Frame(root, takefocus=1, highlightthickness=2)
text  = Entry(frame, width=10, takefocus=1, highlightthickness=2)

root.bind_all('<F1>', displayHelp)
text.bind_class('Entry', '<KeyPress>', lambda e: sayKey(e))
root.bind('<Alt_L>', printWindow)
frame.bind('<Control-Shift-Down>' , cursor)
text.bind('<Control-Shift-Up>', unbindThem)

text.pack()
frame.pack()
text.focus_set()
root.mainloop()



	
