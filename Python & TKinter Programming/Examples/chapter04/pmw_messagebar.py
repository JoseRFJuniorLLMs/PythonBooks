from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('MessageBar')
Pmw.initialise()

messagebar = box = None

def selectionCommand():
    sels = box.getcurselection()
    if len(sels) > 0:
        messagetype = sels[0]
        if messagetype == 'state':
            messagebar.message('state', 'Change of state message')
        else:
            text = messages[messagetype]
            messagebar.message(messagetype, text)

messages = {
            'help'       : 'Save current file',
            'userevent'  : 'Saving file "foo"',
            'busy'       : 'Busy deleting all files from file system ...',
            'systemevent': 'File "foo" saved',
            'usererror'  : 'Invalid file name "foo/bar"',
            'systemerror': 'Failed to save file: file system full',
            }

messagebar = Pmw.MessageBar(root, entry_width=40, entry_relief=GROOVE,
                            labelpos=W, label_text='Status:')
messagebar.pack(side=BOTTOM, fill=X, expand=1, padx=10, pady=10)

box = Pmw.ScrolledListBox(root,	listbox_selectmode=SINGLE,
		items=('state', 'help', 'userevent', 'systemevent',
		       'usererror', 'systemerror', 'busy',),
		label_text='Message type', labelpos=N,
		selectioncommand=selectionCommand)
box.pack(fill=BOTH, expand=1, padx=10, pady=10)


root.mainloop()

