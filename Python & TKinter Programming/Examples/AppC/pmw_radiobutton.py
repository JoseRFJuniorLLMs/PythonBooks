from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('RadioButtons')
Pmw.initialise()

horiz = Pmw.RadioSelect(root, labelpos=W, label_text=HORIZONTAL,
		frame_borderwidth=2, frame_relief=RIDGE)
horiz.pack(fill=X, padx=10, pady=10)

for text in ('Passion fruit', 'Loganberries', 'Mangoes in syrup',
             'Oranges', 'Apples', 'Grapefruit'):
    horiz.add(text)
horiz.invoke('Mangoes in syrup')

multiple = Pmw.RadioSelect(root, labelpos=W, label_text='Multiple\nselection',
		frame_borderwidth=2, frame_relief=RIDGE, selectmode=MULTIPLE)
multiple.pack(fill=X, padx=10)

for text in ('Doug', 'Dinsdale', "Stig O'Tracy", 'Vince', 'Gloria Pules'):
    multiple.add(text)
multiple.invoke('Dinsdale')

root.mainloop()

