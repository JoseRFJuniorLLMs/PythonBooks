from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('PromptDialog')
Pmw.initialise()

dialog = Pmw.PromptDialog(root, title='Password', label_text='Password:',
	    entryfield_labelpos=N, entry_show='*', defaultbutton=0,
	    buttons=('OK', 'Cancel'))

result = dialog.activate()

print 'You selected', result

root.mainloop()

