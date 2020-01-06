from   Tkinter import *
import Pmw
import os
import AppShell
import Image, ImageTk

# Load the PIL plugins for all image types...
for m in ["BmpImagePlugin", "GifImagePlugin", "JpegImagePlugin",
          "PpmImagePlugin", "TiffImagePlugin"]:
    try:
        __import__(m)
    except ImportError:
        pass # ignore missing driver for now
Image._initialized = 1

path = "./icons/"
imgs = "./images/"

class Node:
    def __init__(self, master, tree, icon=None, 
                 openicon=None, name=None, action=None):
        self.master, self.tree = master, tree
        self.icon = PhotoImage(file=icon)
        if openicon:
            self.openicon = PhotoImage(file=openicon)
        else:
            self.openicon = None
        self.width, self.height = 1.5*self.icon.width(), \
                                  1.5*self.icon.height()
        self.name = name
        self.var = StringVar()
        self.var.set(name)
        self.text = Entry(tree, textvariable=self.var, bg=tree.bg,
                          bd=0, width=len(name)+2, font=tree.font,
                          fg=tree.textcolor, insertwidth=1,
                          highlightthickness=1, 
                          highlightbackground=tree.bg,
                          selectbackground="#044484",
                          selectborderwidth=0,
                          selectforeground='white')
        self.action = action
        self.x = self.y = 0  #drawing location
        self.child = []
        self.state = 'colapsed'
        self.selected = 0

    def addChild(self, tree, icon=None, openicon=None, name=None,
                 action=None):    
        child = Node(self, tree, icon, openicon, name, action) 
        self.child.append(child)
        self.tree.display()
        return child         

    def deleteChild(self, child):    
        self.child.remove(child)
        self.tree.display()

    def textForget(self):
        self.text.place_forget()
        for child in self.child:
            child.textForget()                

    def deselect(self):
        self.selected = 0
        for child in self.child:
            child.deselect()

    def boxpress(self, event=None):
        if self.state == 'expanded':
            self.state = 'colapsed'
        elif self.state == 'colapsed':
            self.state = 'expanded'
        self.tree.display()
 
    def invoke(self, event=None):
        if not self.selected:
            self.tree.deselectall()
            self.selected = 1
            self.tree.display()
            if self.action:
                self.action(self.name)
        self.name = self.text.get()
        self.text.config(width=len(self.name)+2)

    def displayIconText(self):
        tree, text = self.tree, self.text
        if self.selected and self.openicon:
            self.pic = tree.create_image(self.x, self.y,
                                         image=self.openicon)
        else:
            self.pic = tree.create_image(self.x, self.y,
                                         image=self.icon)
        text.place(x=self.x+self.width/2, y=self.y, anchor=W)
        text.bind("<ButtonPress-1>", self.invoke)
        tree.tag_bind(self.pic, "<ButtonPress-1>", self.invoke, "+")
        text.bind("<Double-Button-1>", self.boxpress)
        tree.tag_bind(self.pic, "<Double-Button-1>",
                      self.boxpress, "+")

    def displayRoot(self):
        if self.state == 'expanded':                        
            for child in self.child:
                child.display()            
        self.displayIconText()

    def displayLeaf(self):
        self.tree.hline(self.y, self.master.x+1, self.x)
        self.tree.vline(self.master.x, self.master.y, self.y)
        self.displayIconText()

    def displayBranch(self):
        master, tree = self.master, self.tree
        x, y = self.x, self.y            
        tree.hline(y, master.x, x)           
        tree.vline(master.x, master.y, y)
        if self.state == 'expanded' and self.child != []:           
            for child in self.child:
                child.display()                
            box = tree.create_image(master.x, y,
                                    image=tree.minusnode)    
        elif self.state == 'colapsed' and self.child != []: 
            box = tree.create_image(master.x, y,
                                    image=tree.plusnode) 
        tree.tag_bind(box, "<ButtonPress-1>", self.boxpress, "+")
        self.displayIconText()

    def findLowestChild(self, node):
        if node.state == 'expanded' and node.child != []:
            return self.findLowestChild(node.child[-1])
        else:
            return node        

    def display(self):
        master, tree = self.master, self.tree
        n = master.child.index(self)
        self.x = master.x + self.width
        if n == 0:
            self.y = master.y + (n+1)*self.height
        else:    
            previous = master.child[n-1]            
            self.y = self.findLowestChild(previous).y + self.height
        if master == tree:
            self.displayRoot()
        elif master.state == 'expanded':
            if self.child == []:
                self.displayLeaf() 
            else:        
                self.displayBranch()
            tree.lower('line')

class Tree(Canvas):
    def __init__(self, master, icon, openicon, treename, action,
                 bg='white', relief='sunken', bd=2,
                 linecolor='#808080', textcolor='black',
                 font=('MS Sans Serif', 8)):
        Canvas.__init__(self, master, bg=bg, relief=relief, bd=bd,
                        highlightthickness=0)
        self.pack(side='left', anchor=NW, fill='both', expand=1)
        self.bg, self.font= bg, font
        self.linecolor, self.textcolor= linecolor, textcolor
        self.master      = master 
        self.plusnode    = PhotoImage(file=path+'plusnode.gif')
        self.minusnode   = PhotoImage(file=path+'minusnode.gif')
        self.inhibitDraw = 1
        self.imageLabel  = None
        self.imageData   = None
        self.child       = []
        self.x = self.y  = -10
        self.child.append( Node( self, self, action=action,
            icon=icon, openicon=openicon, name=treename) )      

    def display(self):
        if self.inhibitDraw: return
        self.delete(ALL)
        for child in self.child:
            child.textForget()
            child.display()

    def deselectall(self):
        for child in self.child:
            child.deselect()

    def vline(self, x, y, y1):
        for i in range(0, abs(y-y1), 2):
            self.create_line(x, y+i, x, y+i+1, fill=self.linecolor,
                             tags='line')
         
    def hline(self, y, x, x1):
        for i in range(0, abs(x-x1), 2):
            self.create_line(x+i, y, x+i+1, y, fill=self.linecolor,
                             tags='line')

class ImageBrowser(AppShell.AppShell):
    usecommandarea=1
    appname = 'Image Browser'        

    def createButtons(self):
        self.buttonAdd('Ok',
                       helpMessage='Exit',
                       statusMessage='Exit',
                       command=self.quit)
        
    def createMain(self):
        self.panes = self.createcomponent('panes', (), None,
                                          Pmw.PanedWidget,
                                          (self.interior(),),
                                          orient='horizontal')
        self.panes.add('browserpane', min=150, size=160)
        self.panes.add('displaypane', min=.1)
        
        f = path+'folder.gif'
        of = path+'openfolder.gif'
        self.browser = self.createcomponent('browse', (), None,
                                  Tree,
                                  (self.panes.pane('browserpane'),),
                                  icon=f,
                                  openicon=of,
                                  treename='Multimedia',
                                  action=None)
        self.browser.pack(side=TOP, expand=YES, fill=Y)
                            
        self.datasite = self.createcomponent('datasite', (), None,
                                 Frame,
                                 (self.panes.pane('displaypane'),))

        self.datasite.pack(side=TOP, expand=YES, fill=BOTH)
                            
        f  = path+'folder.gif'
        of = path+'openfolder.gif'
        gf = path+'gif.gif'
        jf = path+'jpg.gif'
        xf = path+'other.gif'
    
        self.browser.inhibitDraw = 1
    
        top=self.browser.child[0]
        top.state='expanded'
        jpeg=top.addChild(self.browser,  icon=f, openicon=of,
                          name='Jpeg',  action=None)
        gif=top.addChild(self.browser,   icon=f, openicon=of,
                         name='GIF',   action=None)
        other=top.addChild(self.browser, icon=f, openicon=of,
                           name='Other', action=None)

        imageDir = { '.jpg': (jpeg, jf), '.jpeg': (jpeg, jf),
                     '.gif': (gif, gf),  '.bmp':  (other, xf),
                     '.ppm': (other, xf)}

        files = os.listdir(imgs)
        for file in files:
            r, ext = os.path.splitext(file)
            if ext:
                cont, icon = imageDir.get(ext, (None, None)) 
                if cont:
                    cont.addChild(self.browser, icon=icon,
                                  name=file, action=self.showMe)

        self.browser.inhibitDraw = 0
        self.browser.display()

        self.panes.pack(side=TOP,
                        expand=YES,
                        fill=BOTH)

    def createImageDisplay(self):
        self.imageDisplay = self.createcomponent('image', (), None,
                                                 Label,
                                                 (self.datasite,))
        self.browser.imageLabel = self.imageDisplay
        self.browser.imageData  = None
        self.imageDisplay.place(relx=0.5, rely=0.5, anchor=CENTER)

    def createInterface(self):
        AppShell.AppShell.createInterface(self)
        self.createButtons()
        self.createMain()
        self.createImageDisplay()
        
    def showMe(self, dofile):
        if self.browser.imageData: del self.browser.imageData
        self.browser.imageData = ImageTk.PhotoImage(\
                                     Image.open('%s%s' % \
                                       (imgs, dofile)))
        self.browser.imageLabel['image'] = self.browser.imageData

if __name__ == '__main__':
    imageBrowser = ImageBrowser()
    imageBrowser.run()



