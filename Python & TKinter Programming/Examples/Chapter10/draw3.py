from   Tkinter import *
import Pmw, AppShell, math, time, string

class ToolBarButton(Label):
    def __init__(self, top, parent, tag=None, image=None, command=None,
                 statushelp='', balloonhelp='', height=21, width=21,
                 bd=1, activebackground='lightgrey', padx=0, pady=0,
                 state='normal', bg='grey'):
        Label.__init__(self, parent, height=height, width=width,
                       relief='flat', bd=bd, bg=bg)
        self.bg = bg 
        self.activebackground = activebackground
        if image != None:
            if string.splitfields(image, '.')[1] == 'bmp':
                self.Icon = BitmapImage(file='icons/%s' % image)
            else:
                self.Icon = PhotoImage(file='icons/%s' % image)
        else:
                self.Icon = PhotoImage(file='icons/blank.gif')
        self.config(image=self.Icon)
        self.tag = tag
        self.icommand = command
        self.command  = self.activate
        self.bind("<Enter>",           self.buttonEnter)
        self.bind("<Leave>",           self.buttonLeave)
        self.bind("<ButtonPress-1>",   self.buttonDown)
        self.bind("<ButtonRelease-1>", self.buttonUp)
        self.pack(side='left', anchor=NW, padx=padx, pady=pady)
        if balloonhelp or statushelp:
            top.balloon().bind(self, balloonhelp, statushelp)
        self.state = state
      
    def activate(self):
        self.icommand(self.tag)

    def buttonEnter(self, event):
        if self.state != 'disabled':
            self.config(relief='raised', bg=self.bg)

    def buttonLeave(self, event):
        if self.state != 'disabled':
            self.config(relief='flat', bg=self.bg)

    def buttonDown(self, event):
        if self.state != 'disabled':
            self.config(relief='sunken', bg=self.activebackground)
    
    def buttonUp(self, event):
        if self.state != 'disabled':
            if self.command != None:
                self.command()
            time.sleep(0.05)
            self.config(relief='flat', bg=self.bg)  

class Draw(AppShell.AppShell):
    usecommandarea = 1
    appname        = 'Drawing Program - Version 3'        
    frameWidth     = 840
    frameHeight    = 600
    
    def createButtons(self):
        self.buttonAdd('Postscript',
              helpMessage='Save current drawing (as PostScript)',
              statusMessage='Save drawing as PostScript file',
              command=self.ipostscript)
        self.buttonAdd('Refresh', helpMessage='Refresh drawing',
              statusMessage='Redraw the screen', command=self.redraw)
        self.buttonAdd('Close', helpMessage='Close Screen',
              statusMessage='Exit', command=self.close)
        
    def createBase(self):
        self.toolbar = self.createcomponent('toolbar', (), None,
                  Frame, (self.interior(),), background="gray90")
        self.toolbar.pack(fill=X)

        self.canvas = self.createcomponent('canvas', (), None,
                  Canvas, (self.interior(),), background="white")
        self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)

	Widget.bind(self.canvas, "<Button-1>", self.mouseDown)
 	Widget.bind(self.canvas, "<Button1-Motion>", self.mouseMotion)
 	Widget.bind(self.canvas, "<Button1-ButtonRelease>", self.mouseUp)
        self.root.bind("<KeyPress>", self.setRegular)
        self.root.bind("<KeyRelease>", self.setRegular)

    def setRegular(self, event):
        if event.type == '2' and event.keysym == 'Shift_L':
            self.regular = TRUE
        else:
            self.regular = FALSE

    def createTools(self):
        self.func = {}
        ToolBarButton(self, self.toolbar, 'sep', 'sep.gif',
                      width=10, state='disabled')
        for key, func, balloon in [
                ('pointer', None,                'Edit drawing'),
                ('draw',    self.drawFree,       'Draw freehand'),
                ('smooth',  self.drawSmooth,     'Smooth freehand'),
                ('line',    self.drawLine,       'Rubber line'),
                ('rect',    self.drawRect,       'Unfilled rectangle'),
                ('frect',   self.drawFilledRect, 'Filled rectangle'),
                ('oval',    self.drawOval,       'Unfilled oval'),
                ('foval',   self.drawFilledOval, 'Filled oval')]:
            ToolBarButton(self, self.toolbar, key, '%s.gif' % key,
                          command=self.selectFunc, balloonhelp=balloon,
                               statushelp=balloon)
            self.func[key] = func
            
    def createLineWidths(self):
        ToolBarButton(self, self.toolbar, 'sep', 'sep.gif', width=10,
                      state='disabled')
        for width in ['1', '3', '5']:
            ToolBarButton(self, self.toolbar, width, 'tline%s.gif' %
                          width, command=self.selectWidth,
                          balloonhelp='%s pixel linewidth' % width,
                          statushelp='%s pixel linewidth' % width)

    def createLineColors(self):
        ToolBarButton(self, self.toolbar, 'sep', 'sep.gif', width=10,
                      state='disabled')
        for color in ['black', 'white', 'gray','green',
                      'blue', 'red', 'orange','yellow', 'brown']:
            ToolBarButton(self, self.toolbar, color, 'linecolor.gif',
                   bg=color, command=self.selectForeground,
                   balloonhelp='Draw %s outline' % color,
                   statushelp='Outline will be drawn in %s' % color)

    def createFillColors(self):
        ToolBarButton(self, self.toolbar, 'sep', 'sep.gif', width=10,
                      state='disabled')
        for color in ['black', 'white', 'gray','green',
                      'blue', 'red', 'orange','yellow', 'brown']:
            ToolBarButton(self, self.toolbar, color, 'fillcolor.gif',
                   bg=color, command=self.selectBackground,
                   balloonhelp='Use %s fill color' % color,
                   statushelp='Object will be filled with %s' % color)

    def createPatterns(self):
        ToolBarButton(self, self.toolbar, 'sep', 'sep.gif', width=10,
                      state='disabled')
        for pattern in [None, 'gray12.bmp', 'gray25.bmp',
                        'gray50.bmp', 'gray75.bmp']:
            ToolBarButton(self, self.toolbar, pattern, pattern,
                   command=self.selectPattern,
                   balloonhelp='Stipple pattern',
                   statushelp='Stipple pattern applied to fill')

    def selectFunc(self, tag):
        self.curFunc = self.func[tag]
        if self.curFunc:
            self.canvas.config(cursor='crosshair')
        else:
            self.canvas.config(cursor='arrow')

    def selectWidth(self, tag):
        self.lineWidth = string.atoi(tag)

    def selectBackground(self, tag):
        self.background = tag
        
    def selectForeground(self, tag):
        self.foreground = tag

    def selectPattern(self, tag):
        if tag:
            self.fillStyle='@icons/%s' % tag
        else:
            self.fillStyle = tag
            
    def mouseDown(self, event):
        self.curObject = None
        self.canvas.dtag('drawing')
        self.lineData = []
	self.lastx = self.startx = self.canvas.canvasx(event.x)
	self.lasty = self.starty = self.canvas.canvasy(event.y)
        if not self.curFunc:
            self.selObj = self.canvas.find_closest(self.startx,
                                                   self.starty)[0]
            self.savedWidth = string.atoi(self.canvas.itemcget( \
                                          self.selObj, 'width'))
            self.canvas.itemconfig(self.selObj,
                                   width=self.savedWidth + 2)
            self.canvas.lift(self.selObj)

    def mouseMotion(self, event):
        curx = self.canvas.canvasx(event.x)
        cury = self.canvas.canvasy(event.y)
        prevx = self.lastx
        prevy = self.lasty        
        if self.curFunc:
            self.lastx = curx
            self.lasty = cury

            if self.regular and self.canvas.type('drawing') in \
                   ['oval','rectangle']:
                dx         = self.lastx - self.startx
                dy         = self.lasty - self.starty
                delta = max(dx, dy)
                self.lastx = self.startx + delta
                self.lasty = self.starty + delta
            self.curFunc(self.startx, self.starty, self.lastx,
                 self.lasty, prevx, prevy, self.foreground,
                 self.background, self.fillStyle, self.lineWidth,None)
        else:
            if self.selObj:
                self.canvas.move(self.selObj, curx-prevx, cury-prevy)
                self.lastx = curx
                self.lasty = cury

    def mouseUp(self, event):
        self.prevx = self.lastx
        self.prevy = self.lasty        
	self.lastx = self.canvas.canvasx(event.x)
	self.lasty = self.canvas.canvasy(event.y)

        if self.curFunc:
            if self.regular and self.canvas.type('drawing') in \
                   ['oval','rectangle']:
                dx         = self.lastx - self.startx
                dy         = self.lasty - self.starty
                delta = max(dx, dy)
                self.lastx = self.startx + delta
                self.lasty = self.starty + delta
            self.curFunc(self.startx, self.starty, self.lastx,
                 self.lasty, self.prevx, self.prevy, self.foreground,
                 self.background, self.fillStyle, self.lineWidth,
                 self.lineData)

            self.storeObject()
        else:
            if self.selObj:
                self.canvas.itemconfig(self.selObj,
                                       width=self.savedWidth)

    def drawLine(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.canvas.delete(self.curObject)
        self.curObject =  self.canvas.create_line(x,y,x2,y2,fill=fg,
                              tags='drawing',stipple=fillp,width=wid)

    def drawFree(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.drawFreeSmooth(x,y,x2,y2,x3,y3,FALSE,fg,bg,fillp,wid,ld)

    def drawSmooth(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid, ld):
        self.drawFreeSmooth(x,y,x2,y2,x3,y3,TRUE,fg,bg,fillp,wid,ld)

    def drawFreeSmooth(self,x,y,x2,y2,x3,y3,smooth,fg,bg,fillp,
                       wid,ld):
        if not ld:
            for coord in [[x3, y3, x2, y2], [x2, y2]][smooth]:
                self.lineData.append(coord)
                ild = self.lineData
        else:
            ild = ld
        if len(ild) > 2:
            self.curObject = self.canvas.create_line(ild, fill=fg,
              stipple=fillp, tags='drawing', width=wid, smooth=smooth)

    def drawRect(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.drawFilledRect(x,y,x2,y2,x3,y3,fg,'',fillp,wid,ld)
        
    def drawFilledRect(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.canvas.delete(self.curObject)
        self.curObject =  self.canvas.create_rectangle(x,y,x2,y2,
           outline=fg, tags='drawing',fill=bg,stipple=fillp,width=wid)

    def drawOval(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.drawFilledOval(x,y,x2,y2,x3,y3,fg,'',fillp,wid,ld)
        
    def drawFilledOval(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.canvas.delete(self.curObject)
        self.curObject = self.canvas.create_oval(x,y,x2,y2,outline=fg,
                   fill=bg,tags='drawing',stipple=fillp,width=wid)

    def storeObject(self):
        self.objects.append(( self.startx, self.starty, self.lastx,
             self.lasty, self.prevx,  self.prevy, self.curFunc, 
             self.foreground, self.background, self.fillStyle,
             self.lineWidth, self.lineData ))

    def redraw(self):
        # **** Delete all tags in canvas first ****
        self.canvas.delete(ALL)
        for startx, starty, lastx, lasty, prevx, prevy, func, \
                    fg, bg, fill, lwid, ld,  in self.objects:
            self.curObject = None
            func(startx, starty, lastx, lasty, prevx, prevy,
                 fg, bg, fill, lwid, ld)

    def initData(self):
        self.curFunc    = self.drawLine
        self.curObject  = None
        self.selObj     = None
        self.lineData   = []
        self.savedWidth = 1
        self.objects    = []
        self.foreground = 'black'
        self.background = 'white'
        self.fillStyle  = None
        self.lineWidth  = 1
        self.regular    = FALSE

    def ipostscript(self):
        postscript = self.canvas.postscript()
        fd = open('drawing.ps', 'w')
        fd.write(postscript)
        fd.close()
        
    def close(self):
        self.quit()

    def createInterface(self):
        AppShell.AppShell.createInterface(self)
        self.createButtons()
        self.initData()
        self.createBase()
        self.createTools()
        self.createLineWidths()
        self.createLineColors()
        self.createFillColors()
        self.createPatterns()
        
if __name__ == '__main__':
    draw = Draw()
    draw.run()
