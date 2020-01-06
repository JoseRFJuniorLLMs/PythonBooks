from   Tkinter import *
import Pmw, AppShell, math

class Draw(AppShell.AppShell):
    usecommandarea = 1
    appname        = 'Drawing Program - Version 2'        
    frameWidth     = 800
    frameHeight    = 600
    
    def createButtons(self):
        self.buttonAdd('Close', helpMessage='Close Screen',
              statusMessage='Exit', command=self.close)
        
    def createBase(self):
        self.width  = self.root.winfo_width()-10
        self.height = self.root.winfo_height()-95
        self.command= self.createcomponent('command', (), None,
                   Frame, (self.interior(),), width=self.width*0.25,
                   height=self.height, background="gray90")
        self.command.pack(side=LEFT, expand=YES, fill=BOTH)

        self.canvas = self.createcomponent('canvas', (), None,
                   Canvas, (self.interior(),), width=self.width*0.73,
                   height=self.height, background="white")
        self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)

	Widget.bind(self.canvas, "<Button-1>", self.mouseDown)
 	Widget.bind(self.canvas, "<Button1-Motion>", self.mouseMotion)
 	Widget.bind(self.canvas, "<Button1-ButtonRelease>", self.mouseUp)

	self.radio = Pmw.RadioSelect(self.command, labelpos = None,
                  buttontype = 'radiobutton', orient = 'vertical',
                  command = self.selectFunc, hull_borderwidth = 2,
                  hull_relief = 'ridge',)
	self.radio.pack(side = TOP, expand = 1)

        self.func = {}
	for text, func in (('Select',    None),
                           ('Rectangle', self.drawRect),
                           ('Oval',      self.drawOval),
                           ('Line',      self.drawLine)):
            self.radio.add(text)
            self.func[text] = func
	self.radio.invoke('Rectangle')

    def selectFunc(self, tag):
        self.currentFunc = self.func[tag]
        
    def mouseDown(self, event):
        self.currentObject = None
	self.lastx = self.startx = self.canvas.canvasx(event.x)
	self.lasty = self.starty = self.canvas.canvasy(event.y)
        if not self.currentFunc:
            self.selObj = self.canvas.find_closest(self.startx,
                                                   self.starty)[0]
            self.canvas.itemconfig(self.selObj, width=2)
            self.canvas.lift(self.selObj)

    def mouseMotion(self, event):
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        if self.currentFunc:
            self.lastx = cx
            self.lasty = cy
            self.canvas.delete(self.currentObject)
            self.currentFunc(self.startx, self.starty,
                             self.lastx, self.lasty,
                             self.foreground, self.background)
        else:
            if self.selObj:
                self.canvas.move(self.selObj, cx-self.lastx,
                                 cy-self.lasty)
                self.lastx = cx
                self.lasty = cy

    def mouseUp(self, event):
	self.lastx = self.canvas.canvasx(event.x)
	self.lasty = self.canvas.canvasy(event.y)

        self.canvas.delete(self.currentObject)
        self.currentObject = None
        if self.currentFunc:
            self.currentFunc(self.startx, self.starty,
                             self.lastx, self.lasty,
                             self.foreground, self.background)
        else:
            if self.selObj:
                self.canvas.itemconfig(self.selObj, width=1)

    def drawLine(self, x, y, x2, y2, fg, bg):
        self.currentObject = self.canvas.create_line(x,y,x2,y2,
                                                      fill=fg)

    def drawRect(self, x, y, x2, y2, fg, bg):
        self.currentObject = self.canvas.create_rectangle(x, y,
                                   x2, y2, outline=fg, fill=bg)

    def drawOval(self, x, y, x2, y2, fg, bg):
        self.currentObject = self.canvas.create_oval(x, y, x2, y2,
                                   outline=fg, fill=bg)

    def initData(self):
        self.currentFunc   = None
        self.currentObject = None
        self.selObj        = None
        self.foreground    = 'black'
        self.background    = 'white'

    def close(self):
        self.quit()

    def createInterface(self):
        AppShell.AppShell.createInterface(self)
        self.createButtons()
        self.initData()
        self.createBase()
        
if __name__ == '__main__':
    draw = Draw()
    draw.run()
