from Tkinter       import *
from GUICommon_7_2 import *

import string

class TestColors(Frame, GUICommon):
    def __init__(self, parent=None):

        Frame.__init__(self)
        self.base = "#848484"
        self.pack()
        self.set_colors()
        self.make_widgets()

    def make_widgets(self):
        for tag in ['VDBase', 'DBase', 'Base', 'LBase', 'VLBase']:
            Button(self, text=tag, bg=eval('self.%s' % string.lower(tag)), 
                     fg='white', command=self.quit).pack(side=LEFT)

if __name__ == '__main__':
    TestColors().mainloop()
