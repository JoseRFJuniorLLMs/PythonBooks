from Tkinter       import *
from GUICommon_7_2 import *
from Common_7_2    import *

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
        points = [ '%d-r2,%d+r,%d+r2,%d+r,%d+r+2,%d,%d+r2,%d-r, \
                    %d-r2,%d-r,%d-r-2,%d,%d-r2,%d+r',
                   '%d,%d-r-2,%d+r,%d-r2,%d+r,%d+r2,%d,%d+r+2, \
                    %d-r,%d+r2,%d-r,%d-r2,%d,%d-r-2' ]

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
            self.canv=Canvas(self.frame, width=basesize,  bg=bg,
                             bd=0, height=basesize,
                             highlightthickness=0)
        else:
            self.canv = master    # it was passed in...

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
        exec 'self.hexnut=self.canv.create_polygon(%s, \
                outline=self.dbase, fill=self.lbase)' % pointlist

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

class TestNuts(Frame, GUICommon):
    def __init__(self, parent=None):

        Frame.__init__(self)
        self.pack()
        self.make_widgets()

    def make_widgets(self):
            # List of Metals to create
            metals = [(Color.BRONZE), (Color.CHROME), (Color.BRASS)]

            # List of nut types to display,
            # with sizes and other attributes
            nuts  = [(70, 14, NUT_POINT, 0), (70, 10, NUT_FLAT,  1),
                     (40,  8, NUT_POINT, 0), (100,16, NUT_FLAT,  1)]

            # Iterate for each metal type
            for metal in metals:
                mframe = Frame(self, bg="slategray2")
                mframe.pack(anchor=N, expand=YES, fill=X)

                # Iterate for each of the nuts
                for outside, inset, top, mount in nuts:
                    NUT(mframe, outside=outside, inset=inset,
                        mount=mount, nutbase=metal, 
                        bg="slategray2", 
                        top=top).frame.pack(side=LEFT, 
                                            expand=YES,
                                            padx=1, pady=1)

if __name__ == '__main__':
    TestNuts().mainloop()
