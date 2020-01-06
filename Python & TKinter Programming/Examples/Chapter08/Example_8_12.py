from Tkinter import *
import sys, string

class MakeImageMap:
    def __init__(self, master, file=None):
        self.root = master
        self.root.option_add('*font', ('verdana', 10))
        self.root.title("Create Image Map")
	self.rubberbandBox = None
        self.coordinatedata = []
        self.file = file
        
        self.img = PhotoImage(file=file)
        self.width = self.img.width()
        self.height = self.img.height()

        self.canvas = Canvas(self.root, width=self.width,
                             height=self.height)
        self.canvas.pack(side="top", fill=BOTH, expand='no')
        self.canvas.create_image(0,0,anchor=NW, image=self.img)

        self.frame1 = Frame(self.root, bd=2, relief=RAISED)
        self.frame1.pack(fill=X)
        self.reference = Entry(self.frame1, width=12)
        self.reference.pack(side=LEFT, fill=X, expand='yes')
        self.add = Button(self.frame1, text='Add', command=self.addMap)
        self.add.pack(side=RIGHT, fill=NONE, expand='no')

        self.frame2 = Frame(self.root, bd=2, relief=RAISED)
        self.frame2.pack(fill=X)
        self.done = Button(self.frame2, text='Build ImageMap',
                           command=self.buildMap)
        self.done.pack(side=TOP, fill=NONE, expand='no')
        
	Widget.bind(self.canvas, "<Button-1>", self.mouseDown)
 	Widget.bind(self.canvas, "<Button1-Motion>", self.mouseMotion)
 	Widget.bind(self.canvas, "<Button1-ButtonRelease>", self.mouseUp)

    def mouseDown(self, event):
	self.startx = self.canvas.canvasx(event.x)
	self.starty = self.canvas.canvasy(event.y)

    def mouseMotion(self, event):
	x = self.canvas.canvasx(event.x)
	y = self.canvas.canvasy(event.y)

	if (self.startx != event.x)  and (self.starty != event.y) : 
	    self.canvas.delete(self.rubberbandBox)
	    self.rubberbandBox = self.canvas.create_rectangle(
		self.startx, self.starty, x, y, outline='white',width=2)
	    self.root.update_idletasks()

    def mouseUp(self, event):
	self.endx = self.canvas.canvasx(event.x)
	self.endy = self.canvas.canvasy(event.y)
        self.reference.focus_set()
        self.reference.selection_range(0, END)

    def addMap(self):
        self.coordinatedata.append(self.reference.get(),
                                   self.startx, self.starty,
                                   self.endx, self.endy)
                                         
    def buildMap(self):
        filename = string.splitfields(self.file, '.')[0]
        ofd = open('%s.py' % filename, 'w')
        ifd = open('image1.inp')
        lines = ifd.read()
        ifd.close()
        ofd.write(lines)
        for ref, sx,sy, ex,ey in self.coordinatedata:

            ofd.write("        self.iMap.addRegion(((%5.1f,%5.1f),"
                      "(%5.1f,%5.1f)), '%s')\n" % (sx,sy, ex,ey, ref))
        ofd.write('\n%s\n' % ('#'*70))
        ofd.write('if __name__ == "__main__":\n')
        ofd.write('    root = Tk()\n')
        ofd.write('    root.title("%s")\n' % self.file)
        ofd.write('    imageTest = ImageTest(root, width=%d, height=%d,'
                  'file="%s")\n' % (self.width, self.height, self.file))
        ofd.write('    imageTest.root.mainloop()\n')
        ofd.close()
	self.root.quit()
        
######################################################################
if __name__ == '__main__':
    file = sys.argv[1]
    root = Tk()
    makeImageMap = MakeImageMap(root, file=file)
    makeImageMap.root.mainloop()
