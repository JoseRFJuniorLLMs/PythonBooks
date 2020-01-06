from   Tkinter import *
import Pmw, AppShell, math

from t3ddata import data


class Graph3D(AppShell.AppShell):
    usecommandarea = 1
    appname        = '3-Dimensional Graph'        
    frameWidth     = 800
    frameHeight    = 650
    
    def createButtons(self):
        self.buttonAdd('Print',
              helpMessage='Print current graph (PostScript)',
              statusMessage='Print graph as PostScript file',
              command=self.iprint)
        self.buttonAdd('Close',
              helpMessage='Close Screen',
              statusMessage='Exit',
               command=self.close)
        
    def createBase(self):
        self.width  = self.root.winfo_width()-10
        self.height = self.root.winfo_height()-95
        self.canvas = self.createcomponent('canvas', (), None,
                                           Canvas, (self.interior(),),
                                           width=self.width,
                                           height=self.height,
                                           background="black")
        self.canvas.pack(side=TOP, expand=YES, fill=BOTH)

        self.awid  = int(self.width  * 0.68)
        self.ahgt  = int(self.height * 0.5)
        self.hoff  = self.awid  / 3
        self.voff  = self.ahgt +3
        self.vht   = self.voff / 2
        self.hroff = (self.hoff / self.rows)
        self.vroff = self.voff / self.rows
        self.xincr = float(self.awid) / float(self.steps)
        self.xorg  = self.width/3.7
        self.yorg  = self.height/3
        self.yfac  = float(self.vht) / float(self.maxY-self.minY)

        self.canvas.create_polygon(self.xorg, self.yorg, 
             self.xorg+self.awid, self.yorg,
             self.xorg+self.awid-self.hoff, self.yorg+self.voff,
             self.xorg-self.hoff, self.yorg+self.voff,
             self.xorg, self.yorg, fill='', outline=self.lineColor)

        self.canvas.create_rectangle(self.xorg, self.yorg-self.vht,
             self.xorg+self.awid, self.yorg,
             fill='', outline=self.lineColor)

        self.canvas.create_polygon(self.xorg, self.yorg, 
             self.xorg-self.hoff, self.yorg+self.voff,
             self.xorg-self.hoff, self.yorg+self.voff-self.vht,
             self.xorg, self.yorg-self.vht,
             fill='', outline=self.lineColor)

        self.canvas.create_text(self.xorg-self.hoff-5, self.yorg+self.voff,
             text='%d' % self.minY, fill=self.lineColor, anchor=E)

        self.canvas.create_text(self.xorg-self.hoff-5, self.yorg+self.voff-self.vht,
             text='%d' % self.maxY, fill=self.lineColor, anchor=E)
        
        self.canvas.create_text(self.xorg-self.hoff, self.yorg+self.voff+5,
             text='%d' % self.minX, fill=self.lineColor, anchor=N)

        self.canvas.create_text(self.xorg+self.awid-self.hoff, self.yorg+self.voff+5,
             text='%d' % self.maxX, fill=self.lineColor, anchor=N)

    def initData(self):     
        self.minY        =   0
        self.maxY        = 100
        self.minX        =   0
        self.maxX        = 100
        self.steps       = 100
        self.rows        =  10
        self.spectrum    = Pmw.Color.spectrum(self.steps,
                               saturation=0.8,
                               intensity=0.8, extraOrange=1)
        self.lineColor   = 'gray80'
        self.lowThresh   =  05
        self.highThresh  =  20
        
    def transform(self, base, factor):
        rgb = self.winfo_rgb(base)
        retval = "#"
        for v in [rgb[0], rgb[1], rgb[2]]:
	    v = (v*factor)/256
            if v > 255: v = 255
            if v < 0:   v = 0
            retval = "%s%02x" % (retval, v)
        return retval

    def plotData(self, row, rowdata):
        rootx  = self.xorg - (row*self.hroff)
        rooty  = self.yorg + (row*self.vroff)
        cidx   = 0
        lasthv = self.maxY*self.yfac
        xadj   = float(self.xincr)/4.0
        lowv   = self.lowThresh*self.yfac

        for datum in rowdata:
            lside = datum*self.yfac
            color = self.spectrum[cidx]
            if datum <= self.lowThresh:
                color = self.transform(color, 0.8)
            elif datum >= self.highThresh:
                color = self.transform(color, 1.2)
                
            self.canvas.create_polygon(rootx, rooty, rootx, rooty-lside,
                        rootx-self.hroff, rooty-lside+self.vroff,
                        rootx-self.hroff, rooty+self.vroff,
                        rootx, rooty, fill=color, outline=color,
                        width=self.xincr)
            base = min(min(lside, lasthv), lowv)
            self.canvas.create_line(rootx-xadj, rooty-lside,
                        rootx-xadj-self.hroff, rooty-lside+self.vroff,
                        rootx-xadj-self.hroff, rooty+self.vroff-base,
                        fill='black', width=1)
            lasthv = lowv = lside
            
            cidx = cidx + 1
            rootx = rootx + self.xincr

    def demo(self):
        for i in range(self.rows):
            self.plotData(i, data[i])
            self.root.update()

    def iprint(self):
        pass
    
    def close(self):
        self.quit()

    def createInterface(self):
        AppShell.AppShell.createInterface(self)
        self.createButtons()
        self.initData()
        self.createBase()
        
if __name__ == '__main__':
    graph = Graph3D()
    graph.root.after(100, graph.demo)
    graph.run()










