from Tkinter import *
from imagemap import *

class ImageTest:
    def hit(self, event):
        self.infoVar.set(self.iMap.getRegion(event.x, event.y))

    def __init__(self, master, width=0, height=0, file=None):
        self.root = master
        self.root.option_add('*font', ('verdana', 12, 'bold'))
        self.iMap = ImageMap()
        
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack(side="top", fill=BOTH, expand='no')

        self.img = PhotoImage(file=file)
        self.canvas.create_image(0,0,anchor=NW, image=self.img)
        self.canvas.bind('<Button-1>', self.hit)
        self.infoVar = StringVar()
        self.info = Entry(self.root, textvariable=self.infoVar)
        self.info.pack(fill=X)

        self.iMap.addRegion(((144.0,382.0),(176.0,398.0)), '')

######################################################################
if __name__ == "__main__":
    root = Tk()
    root.title("calculator.gif")
    imageTest = ImageTest(root, width=237, height=513,file="calculator.gif")
    imageTest.root.mainloop()
