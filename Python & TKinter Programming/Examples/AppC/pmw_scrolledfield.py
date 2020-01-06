from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('ScrolledField')
Pmw.initialise()

lines = (
  "Mount Everest.  Forbidding, aloof, terrifying.  This year, this",
  "remote Himalayan mountain, this mystical temple, surrounded by the",
  "most difficult terrain in the world, repulsed yet another attempt to",
  "conquer it.  (Picture changes to wind-swept, snowy tents and people)",
  "This time, by the International Hairdresser's Expedition.  In such",
  "freezing, adverse conditions, man comes very close to breaking",
  "point.  What was the real cause of the disharmony which destroyed",
  "their chances at success?")
 
global index
field = index = None

def execute():
    global index
    field.configure(text=lines[index % len(lines)])
    index = index + 1

field = Pmw.ScrolledField(root, entry_width=30,
            entry_relief=GROOVE, labelpos=N,
            label_text='Scroll the field using the\nmiddle mouse button')
field.pack(fill=X, expand=1, padx=10, pady=10)

button = Button(root, text='Change field', command=execute)
button.pack(padx=10, pady=10)

index = 0
execute()

root.mainloop()



