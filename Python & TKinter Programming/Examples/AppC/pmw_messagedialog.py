from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('MessageDialog')
Pmw.initialise()

dialog = Pmw.MessageDialog(root, title = 'Simple Dialog',
                   defaultbutton = 0,
                   buttons = ('OK', 'Apply', 'Cancel', 'Help'),
                   message_text = 'This dialog box was constructed on demand')
dialog.iconname('Simple message dialog')
result = dialog.activate()

print 'You selected', result

root.mainloop()

