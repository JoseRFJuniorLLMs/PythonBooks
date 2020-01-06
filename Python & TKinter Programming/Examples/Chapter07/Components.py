from Tkinter   import *
from GUICommon import *
from Common    import *

class LED(GUICommon): 
    def __init__(self, master=None, width=25, height=25, 
                 appearance=FLAT,
                 status=STATUS_ON, bd=1, 
                 bg=None, 
                 shape=SQUARE, outline="",
                 blink=0, blinkrate=1,
                 orient=POINT_UP,
                 takefocus=0):
        # preserve attributes
        self.master       = master
        self.shape        = shape
        self.Colors       = [None, Color.OFF, Color.ON,
                             Color.WARN, Color.ALARM, '#00ffdd']
        self.status       = status
        self.blink        = blink
        self.blinkrate    = int(blinkrate)
        self.on           = 0
        self.onState      = None

        if not bg:
            bg = Color.PANEL

        ## Base frame to contain light
        self.frame=Frame(master, relief=appearance, bg=bg, bd=bd, 
                         takefocus=takefocus)

        basesize = width
        d = center = int(basesize/2)

        if self.shape == SQUARE:
            self.canvas=Canvas(self.frame, height=height, width=width, 
                               bg=bg, bd=0, highlightthickness=0)

            self.light=self.canvas.create_rectangle(0, 0, width, height,
                                                    fill=Color.ON)
        elif self.shape == ROUND:
            r = int((basesize-2)/2)
            self.canvas=Canvas(self.frame, width=width, height=width, 
                               highlightthickness=0,
                               bg=bg, bd=0)
            if bd > 0:
                self.border=self.canvas.create_oval(center-r, center-r, 
                                                    center+r, center+r)
                r = r - bd
            self.light=self.canvas.create_oval(center-r-1, center-r-1, 
                                               center+r, center+r, 
                                               fill=Color.ON,
                                               outline=outline)
        else:  # Default is an ARROW
            self.canvas=Canvas(self.frame, width=width, height=width, 
                               highlightthickness=0, 
                               bg=bg, bd=0)
            x = d
            y = d
            VL = ARROW_HEAD_VERTICES[orient] 
            self.light=self.canvas.create_polygon(eval(VL[0]),
                              eval(VL[1]), eval(VL[2]), eval(VL[3]),
                              eval(VL[4]), eval(VL[5]), eval(VL[6]),
                              eval(VL[7]), outline = outline)

        self.canvas.pack(side=TOP, fill=X, expand=NO)
        self.update()

    def update(self):
        # First do the blink, if set to blink
        if self.blink:
            if self.on:
                if not self.onState:
                    self.onState = self.status
                self.status  = STATUS_OFF
                self.on      = 0                            
            else:
                if self.onState:
                    self.status = self.onState     # Current ON color
                self.on = 1

        # Set color for current status
        self.canvas.itemconfig(self.light, fill=self.Colors[self.status])

        self.canvas.update_idletasks()

        if self.blink:
            self.frame.after(self.blinkrate * 1000, self.update)

# ##########################################################################
# The HEXNUT class creates a Nut object. Several options are available:
# If 'frame' is TRUE, the caller requires the nut to be placed in a frame:
# If 'frame' is FALSE, the nut is to be drawn on the canvas passed as
# 'master' at coordinates 'x' and 'y'. If 'mount' is TRUE, the nut will be 
# enclosed by a mounting hole.  'outside' specifies the outside diameter 
# in pixels and 'inset' specifies # the internal offset (for the threads)
# 'nutbase' is the base color for the nut. 'top' specifies whether the nut
# is aligned with a point on top or with a flat (Fussy, I know!)
# ##########################################################################

class HEXNUT(GUICommon):
    def __init__(self, master, frame=1, mount=1, outside=70, inset=8, 
                 bg=Color.PANEL, nutbase=Color.BRONZE,
                 top=NUT_FLAT, takefocus=0, x=-1, y=-1): 
        points = [ '%d-r2,%d+r,%d+r2,%d+r,%d+r+2,%d,%d+r2,%d-r,%d-r2,\
                    %d-r,%d-r-2,%d,%d-r2,%d+r',
                   '%d,%d-r-2,%d+r,%d-r2,%d+r,%d+r2,%d,%d+r+2,%d-r,%d+r2,\
                    %d-r,%d-r2,%d,%d-r-2' ]

        self.base   = nutbase
        self.status = STATUS_OFF
        self.blink  = 0
        self.set_colors()

        basesize = outside+4
        if frame:
            self.frame = Frame(master, relief="flat", bg=bg, bd=0, 
                               highlightthickness=0,
                               takefocus=takefocus)
            self.frame.pack(expand=0)
            self.canv=Canvas(self.frame, width=basesize,
                             height=basesize, 
                             highlightthickness=0,
                             bg=bg, bd=0)
        else:
            self.canv = master    # it go passed in...

        center = basesize/2
        if x >= 0:
            centerx = x
            centery = y
        else:
            centerx = centery = center

        r = outside/2

        ## First, draw the mount, if needed
        if mount:
            self.mount=self.canv.create_oval(centerx-r, centery-r,
                                             centerx+r, centery+r, 
                                             fill=self.dbase, 
                                             outline=self.vdbase)
        ## Next, draw the hex nut
        r  = r - (inset/2)
        r2 = r/2
        pointlist = points[top] % (centerx,centery,centerx,centery,
                                   centerx,centery,centerx,centery,
                                   centerx,centery,centerx,centery,
                                   centerx,centery)
        print pointlist
	print eval(pointlist)
        setattr(self, 'hexnut', self.canv.create_polygon(eval(pointlist), 
                            outline=self.dbase, fill=self.lbase))

        ## Now, the inside edge of the threads
        r = r - (inset/2)
        self.canv.create_oval(centerx-r, centery-r,
                              centerx+r, centery+r, 
                              fill=self.lbase, outline=self.vdbase)

        ## Finally, the background showing through the hole
        r = r - 2
        self.canv.create_oval(centerx-r, centery-r,
                              centerx+r, centery+r, 
                              fill=bg, outline="")

        self.canv.pack(side="top", fill='x', expand='no')

class NUT(Frame, HEXNUT):
    def __init__(self, master, outside=70, inset=8, frame=1, mount=1, 
                 bg="gray50", nutbase=Color.CHROME, top=NUT_FLAT):
        Frame.__init__(self)
        HEXNUT.__init__(self, master=master, outside=outside, 
                        inset=inset, frame=frame, mount=mount, 
                        bg=bg, nutbase=nutbase, top=top)

class TOGGLESWITCH(Frame, HEXNUT):
    def __init__(self, master, outside=70, inset=8, bg=Color.PANEL, 
                 nutbase=Color.CHROME, mount=1, frame=1, 
                 top=NUT_POINT, mode=MODE_US, status=STATUS_ON):
        Frame.__init__(self)
        HEXNUT.__init__(self, master=master, outside=outside+40, 
                        inset=35, frame=frame, mount=mount, 
                        bg=bg, nutbase=nutbase, top=top)

        self.status = status
        self.mode   = mode
        self.center = (outside+44)/2
        self.r      = (outside/2)-4

        ## First Fill in the center
        self.r1=self.canv.create_oval(self.center-self.r,
                                      self.center-self.r, 
                                      self.center+self.r,
                                      self.center+self.r, 
                                      fill=self.vdbase,
                                      outline=self.dbase, 
                                      width=1)
        self.update()  ## The rest is dependent on the on/off state

    def update(self):
        self.canv.delete('lever')   ## Remove any previous toggle lever
        direction = POINT_UP
        if (self.mode == MODE_UK and self.status == STATUS_ON) or \
           (self.mode == MODE_US and self.status == STATUS_OFF):
            direction = POINT_DOWN

        # now update the status
        if direction == POINT_UP:
            ## Draw the toggle lever
            self.p1=self.canv.create_polygon(self.center-self.r,
                                             self.center, 
                                             self.center-self.r-3, 
                                             self.center-(4*self.r),
                                             self.center+self.r+3,
                                             self.center-(4*self.r), 
                                             self.center+self.r, 
                                             self.center,
                                             fill=self.dbase,
                                             outline=self.vdbase, 
                                             tags="lever")
            centerx = self.center
            centery = self.center - (4*self.r)
            r = self.r + 2
            ## Draw the end of the lever
            self.r2=self.canv.create_oval(centerx-r, centery-r,
                                          centerx+r, 
                                          centery+r, 
                                          fill=self.base,
                                          outline=self.vdbase, 
                                          width=1, tags="lever")
            centerx = centerx - 1
            centery = centery - 3
            r = r / 3
            ## Draw the highlight
            self.r2=self.canv.create_oval(centerx-r, centery-r,
                                          centerx+r, 
                                          centery+r, 
                                          fill=self.vlbase,
                                          outline=self.lbase, 
                                          width=2, tags="lever")

        else:
            ## Draw the toggle lever
            self.p1=self.canv.create_polygon(self.center-self.r,
                                             self.center, 
                                             self.center-self.r-3, 
                                             self.center+(4*self.r),
                                             self.center+self.r+3,
                                             self.center+(4*self.r), 
                                             self.center+self.r,
                                             self.center,
                                             fill=self.dbase, 
                                             outline=self.vdbase, 
                                             tags="lever")
            centerx = self.center
            centery = self.center + (4*self.r)
            r = self.r + 2
            ## Draw the end of the lever
            self.r2=self.canv.create_oval(centerx-r, centery-r,
                                          centerx+r, 
                                          centery+r, 
                                          fill=self.base,
                                          outline=self.vdbase,
                                          width=1, tags="lever")
            centerx = centerx - 1
            centery = centery - 3
            r = r / 3
            ## Draw the highlight
            self.r2=self.canv.create_oval(centerx-r, centery-r,
                                          centerx+r, 
                                          centery+r, 
                                          fill=self.vlbase,
                                          outline=self.lbase,
                                          width=2, tags="lever")

        self.canv.update_idletasks()

