from   Tkinter import *
import Pmw, AppShell, math

class EndObject:
    def __init__(self, canvas=None, function=None, background='white',
		 foreground='black', x0=0, y0=0, x1=100, x1=100):
        self.canvas = canvas
	self.func = function
	self.bg = background
	self.fg = foreground
	self.x0 = x0
	self.y0 = y0
	self.x1 = x1
	self.y1 = y1
	self.centerX = self.x0 + ((self.x1 - self.x0)/2.0)
	self.centerY = self.y0 + ((self.y1 - self.y0)/2.0)	
	self.connector = None

    def setConnector(self, connector):
        self.connector = connector

    def draw(self):
        apply(self.func, (self, self.x0, self.y0, self.x1, self.y1,
			  self.fg, self.bg))

class Connector:
    def __init__(self, canvas=None, function=None, color='blue',
		 end1=None, end2=None):
        self.canvas = canvas
	self.func = function
	self.fill = fill
        self.end1 = end1
	self.end2 = end2

class Draw(AppShell.AppShell):
	usecommandarea = 1
	appname	       = 'Drawing Program - Version 1'	      
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

	def drawLine(self, x, y, x2, y2, fg, bg):
		self.currentObject = self.canvas.create_line(x,y,x2,y2,
						     fill=fg)

	def drawRect(self, x, y, x2, y2, fg, bg):
		self.currentObject = self.canvas.create_rectangle(x, y,
					      x2, y2, outline=fg, fill=bg)

	def drawOval(self, x, y, x2, y2, fg, bg):
		self.currentObject =  self.canvas.create_oval(x, y, x2, y2,
				      outline=fg, fill=bg)

	def initData(self):
		self.currentFunc   = None
		self.currentObject = None
		self.selObj	   = None
		self.foreground	   = 'black'
		self.background	   = 'white'

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
