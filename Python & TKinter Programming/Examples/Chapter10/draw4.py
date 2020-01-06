from   Tkinter import *
import Pmw, AppShell, math, time, string, marshal
from cursornames import *
from toolbarbutton import ToolBarButton
from tkFileDialog import *

transDict = { 'bx': 'boundX', 'by': 'boundY',
              'x':  'adjX',   'y':  'adjY',
              'S':  'uniqueIDINT' }

class Draw(AppShell.AppShell):
    usecommandarea = 1
    appname        = 'Drawing Program - Version 4'
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

    def createMenus(self):
        self.menuBar.deletemenuitems('File')
        self.menuBar.addmenuitem('File', 'command', 'New drawing',
                                 label='New', command=self.newDrawing)
        self.menuBar.addmenuitem('File', 'command', 'Open drawing',
                                 label='Open...', command=self.openDrawing)
        self.menuBar.addmenuitem('File', 'command', 'Save drawing',
                                 label='Save', command=self.saveDrawing)
        self.menuBar.addmenuitem('File', 'command', 'Save drawing',
                                 label='SaveAs...', command=self.saveAsDrawing)
        self.menuBar.addmenuitem('File', 'separator')
        self.menuBar.addmenuitem('File', 'command', 'Exit program',
                                 label='Exit', command=self.quit)

    def createTools(self):
        self.func      = {}
        self.transFunc = {}
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
            self.func[key]       = func
            self.transFunc[func] = key
            
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
        self.uniqueID = 'S*%d' % self.serial
        self.serial = self.serial + 1
        if not self.curFunc:
            if event.widget.find_withtag(CURRENT):
                tags = self.canvas.gettags(CURRENT)
                for tag in tags:
                    if tag[:2] == 'S*':
                        objectID = tag
                if 'grabHandle' in tags:
                    self.inGrab      = TRUE
                    self.releaseGrab = FALSE
                    self.uniqueID    = objectID
                else:
                    self.inGrab = FALSE
                    self.addGrabHandles(objectID, 'grab')
                    self.canvas.config(cursor='fleur')
                    self.uniqueID = objectID
        else:
            self.canvas.delete("grabHandle")
            self.canvas.dtag("grabHandle")
            self.canvas.dtag("grab")                
            
    def mouseMotion(self, event):
        curx = self.canvas.canvasx(event.x)
        cury = self.canvas.canvasy(event.y)
        prevx = self.lastx
        prevy = self.lasty        
        if not self.inGrab and self.curFunc:
            self.lastx = curx
            self.lasty = cury
            if self.regular and self.curFunc in \
                   [self.func['oval'], self.func['rect'],
                    self.func['foval'],self.func['frect']]:
                dx         = self.lastx - self.startx
                dy         = self.lasty - self.starty
                delta = max(dx, dy)
                self.lastx = self.startx + delta
                self.lasty = self.starty + delta
            self.curFunc(self.startx, self.starty, self.lastx,
                 self.lasty, prevx, prevy, self.foreground,
                 self.background, self.fillStyle, self.lineWidth,None)
        else:
            if self.inGrab:
                self.canvas.delete("grabbedObject")                
                self.canvas.dtag("grabbedObject")                
                tags = self.canvas.gettags(CURRENT)
                for tag in tags:
                    if '*' in tag:
                        key, value = string.split(tag, '*')
                        var = transDict[key]
                        setattr(self, var, string.atoi(value))
                self.uniqueID = 'S*%d' % self.uniqueIDINT
                x1, y1, x2, y2, px, py, self.growFunc, \
                   fg, bg, fill, lwid, ld= self.objects[self.uniqueID]
                if self.boundX == 1 and self.adjX:
                    x1 =  x1 + curx-prevx
                elif self.boundX == 2 and self.adjX:
                    x2 =  x2 + curx-prevx
                if self.boundY == 1 and self.adjY:
                    y1 = y1 + cury-prevy
                elif self.boundY == 2 and self.adjY:
                    y2 = y2 + cury-prevy
                self.growFunc(x1,y1,x2,y2,px,py,fg,bg,fill,lwid,ld)
                self.canvas.addtag_withtag("grabbedObject",
                                           self.uniqueID)
                self.storeObject(x1,y1,x2,y2,px,py,self.growFunc,
                                 fg,bg,fill,lwid,ld)
                self.lastx = curx
                self.lasty = cury
            else:
                self.canvas.move('grab', curx-prevx, cury-prevy)
                self.lastx = curx
                self.lasty = cury

    def mouseUp(self, event):
        self.prevx = self.lastx
        self.prevy = self.lasty        
        self.lastx = self.canvas.canvasx(event.x)
        self.lasty = self.canvas.canvasy(event.y)

        if self.curFunc:
            if self.regular and self.curFunc in \
                   [self.func['oval'], self.func['rect'],
                    self.func['foval'],self.func['frect']]:
                dx = self.lastx - self.startx
                dy = self.lasty - self.starty
                delta = max(dx, dy)
                self.lastx = self.startx + delta
                self.lasty = self.starty + delta
            self.curFunc(self.startx, self.starty, self.lastx,
                 self.lasty, self.prevx, self.prevy, self.foreground,
                 self.background, self.fillStyle, self.lineWidth,
                 self.lineData)
            self.inGrab      = FALSE
            self.releaseGrab = TRUE
            self.growFunc    = None
            self.storeObject(self.startx, self.starty, self.lastx,
                 self.lasty, self.prevx, self.prevy, self.curFunc, 
                 self.foreground, self.background, self.fillStyle,
                 self.lineWidth, self.lineData)
        else:
            if self.inGrab:
                tags = self.canvas.gettags(CURRENT)
                for tag in tags:
                    if '*' in tag:
                        key, value = string.split(tag, '*')
                        var = transDict[key]
                        setattr(self, var, string.atoi(value))
                x1,y1,x2,y2, px, py, self.growFunc, \
                    fg,bg,fill,lwid,ld = self.objects[self.uniqueID]
                if self.boundX == 1 and self.adjX:
                    x1 =  x1 + self.lastx-self.prevx
                elif self.boundX == 2 and self.adjX:
                    x2 =  x2 + self.lastx-self.prevx
                if self.boundY == 1 and self.adjY:
                    y1 = y1 + self.lasty-self.prevy
                elif self.boundY == 2 and self.adjY:
                    y2 = y2 + self.lasty-self.prevy
                self.growFunc(x1,y1,x2,y2,px,py,fg,bg,fill,lwid,ld)
                self.storeObject(x1,y1,x2,y2,px,py,self.growFunc,
                                 fg,bg,fill,lwid,ld)
                self.addGrabHandles(self.uniqueID, self.uniqueID)
            if self.selObj:
                self.canvas.itemconfig(self.selObj,
                                       width=self.savedWidth)
        self.canvas.config(cursor='arrow')
        
    def addGrabHandles(self, objectID, tag):
        self.canvas.delete("grabHandle")
        self.canvas.dtag("grabHandle")
        self.canvas.dtag("grab")                
        self.canvas.dtag("grabbedObject")                

        self.canvas.addtag("grab", "withtag", CURRENT)
        self.canvas.addtag("grabbedObject", "withtag", CURRENT)
        x1,y1,x2,y2 = self.canvas.bbox(tag)
        for x,y, curs, tagBx, tagBy, tagX, tagY in [
                (x1,y1,TLC,            'bx*1','by*1','x*1','y*1'),
                (x2,y1,TRC,            'bx*2','by*1','x*1','y*1'),
                (x1,y2,BLC,            'bx*1','by*2','x*1','y*1'),
                (x2,y2,BRC,            'bx*2','by*2','x*1','y*1'),
                (x1+((x2-x1)/2),y1,TS, 'bx*0','by*1','x*0','y*1'),
                (x2,y1+((y2-y1)/2),RS, 'bx*2','by*0','x*1','y*0'),
                (x1,y1+((y2-y1)/2),LS, 'bx*1','by*0','x*1','y*0'),
                (x1+((x2-x1)/2),y2,BS, 'bx*0','by*2','x*0','y*1')]:
            ghandle = self.canvas.create_rectangle(x-2,y-2,x+2,y+2,
                      outline='black', fill='black', tags=('grab',
                      'grabHandle','%s'%tagBx,'%s'%tagBy,'%s'%tagX,
                      '%s'%tagY,'%s'%objectID))
            self.canvas.tag_bind(ghandle, '<Any-Enter>',
                      lambda e, s=self, c=curs: s.setCursor(e,c))
            self.canvas.tag_bind(ghandle, '<Any-Leave>',
                                 self.resetCursor)
            self.canvas.lift("grab")

    def setCursor(self, event, cursor):
        self.savedCursor = self.canvas.cget('cursor')
        self.canvas.config(cursor=cursor)

    def resetCursor(self, event):
        if self.releaseGrab and self.savedCursor:
            self.canvas.config(cursor=self.savedCursor)  

    def drawLine(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.canvas.delete(self.curObject)
        self.curObject = self.canvas.create_line(x,y,x2,y2,
                tags=self.uniqueID, fill=fg,stipple=fillp,width=wid)

    def drawFree(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.drawFreeSmooth(x,y,x2,y2,x3,y3,FALSE,fg,bg,fillp,wid,ld)

    def drawSmooth(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
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
              stipple=fillp,tags=self.uniqueID,width=wid,smooth=smooth)

    def drawRect(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.drawFilledRect(x,y,x2,y2,x3,y3,fg,'',fillp,wid,ld)
        
    def drawFilledRect(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.canvas.delete(self.curObject)
        self.curObject = self.canvas.create_rectangle(x,y,x2,y2,
                   tags=self.uniqueID,outline=fg,fill=bg,
                   stipple=fillp, width=wid)

    def drawOval(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.drawFilledOval(x,y,x2,y2,x3,y3,fg,'',fillp,wid,ld)
        
    def drawFilledOval(self,x,y,x2,y2,x3,y3,fg,bg,fillp,wid,ld):
        self.canvas.delete(self.curObject)
        self.curObject = self.canvas.create_oval(x,y,x2,y2,
                   tags=self.uniqueID,outline=fg,fill=bg,
                   stipple=fillp,width=wid)

    def storeObject(self, x1,y1,x2,y2,px,py,func,fg,bg,fill,lwid,ld):
        self.objects[self.uniqueID] = ( x1,y1,x2,y2,px,py,func,fg,bg,
                                        fill,lwid,ld )

    def redraw(self):
        # **** Delete all tags in canvas first ****
        self.canvas.delete(ALL)
        keys = self.objects.keys()
        keys.sort()
        for key in keys:
            startx, starty, lastx, lasty, prevx, prevy, func, \
                    fg, bg, fill, lwid , ld= self.objects[key]
            self.curObject = None
            self.uniqueID = key
            func(startx, starty, lastx, lasty, prevx, prevy,
                 fg, bg, fill, lwid, ld)

    def newDrawing(self):
        self.canvas.delete(ALL)
        self.initData()

    def openDrawing(self):
        ofile = askopenfilename(filetypes=[("PTkP Draw", "ptk"),
                                           ("All Files", "*")])
        if ofile:
            self.currentName = ofile
            self.initData()
            fd = open(ofile)
            items = marshal.load(fd)
            for i in range(items):
                self.uniqueID, x1,y1,x2,y2,px,py,cfunc, \
                     fg,bg,fill,lwid,ld = marshal.load(fd)
                self.storeObject(x1,y1,x2,y2,px,py,self.func[cfunc],
                                 fg,bg,fill,lwid,ld)
            fd.close()
        self.redraw()
        
    def saveDrawing(self):
        self.doSave()

    def saveAsDrawing(self):
        ofile = asksaveasfilename(filetypes=[("PTkP Draw", "ptk"),
                                             ("All Files", "*")])
        if ofile:
            self.currentName = ofile
            self.doSave()
            
    def doSave(self):
        fd = open(self.currentName, 'w')
        keys = self.objects.keys()
        keys.sort()
        marshal.dump(len(keys), fd)
        for key in keys:
            startx, starty, lastx, lasty, prevx, prevy, func, \
                    fg, bg, fill, lwid , ld= self.objects[key]
            cfunc = self.transFunc[func]
            marshal.dump((key, startx, starty, lastx, lasty, prevx, \
                          prevy, cfunc, fg, bg, fill, lwid , ld), fd)
        fd.close()
        
    def initData(self):
        self.curFunc     = self.drawLine
        self.growFunc    = None
        self.curObject   = None
        self.selObj      = None
        self.lineData   = []
        self.savedWidth  = 1
        self.savedCursor = None
        self.objects     = {}       # Now a dictionary
        self.foreground  = 'black'
        self.background  = 'white'
        self.fillStyle   = None
        self.lineWidth   = 1
        self.serial      = 1000
        self.regular     = FALSE
        self.inGrab      = FALSE
        self.releaseGrab = TRUE
        self.currentName = 'Untitled'

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
        self.createMenus()
        self.createBase()
        self.createTools()
        self.createLineWidths()
        self.createLineColors()
        self.createFillColors()
        self.createPatterns()
        
if __name__ == '__main__':
    draw = Draw()
    draw.run()
