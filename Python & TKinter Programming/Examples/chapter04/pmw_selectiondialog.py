from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('SelectionDialog')
Pmw.initialise()

dialog = None

def execute(result):
    sels = dialog.getcurselection()
    if len(sels) == 0:
        print 'You clicked on', result, '(no selection)'
    else:
        print 'You clicked on', result, sels[0]
    dialog.deactivate(result)

dialog = Pmw.SelectionDialog(root, title='String',
	    buttons=('OK', 'Cancel'), defaultbutton='OK',
	    scrolledlist_labelpos=N, label_text='Who sells string?',
	    scrolledlist_items=('Mousebat', 'Follicle', 'Goosecreature',
                      'Mr. Simpson', 'Ampersand', 'Spong', 'Wapcaplet',
                      'Looseliver', 'Vendetta', 'Prang'),
	    command=execute)
dialog.activate()

root.mainloop()

