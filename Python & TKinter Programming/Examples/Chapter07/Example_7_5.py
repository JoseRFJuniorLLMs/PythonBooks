from Tkinter     import *
from GUICommon   import *
from Common      import *
from Example_7_4 import HEXNUT

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

class TestSwitches(Frame, GUICommon):
    def __init__(self, parent=None):

        Frame.__init__(self)
        self.pack()
        self.make_widgets()

    def make_widgets(self):
            # List of Metals to create
            metals = [(Color.BRONZE), (Color.CHROME), (Color.BRASS)]

            # List of switchesdisplay, with sizes and other attributes
            switches = [(NUT_POINT, 0, STATUS_OFF, MODE_US),
                        (NUT_FLAT,  1, STATUS_ON,  MODE_US),
                        (NUT_FLAT,  0, STATUS_ON,  MODE_UK),
                        (NUT_POINT, 0, STATUS_OFF, MODE_UK)]

            # Iterate for each metal type
            for metal in metals:
                mframe = Frame(self, bg="slategray2")
                mframe.pack(anchor=N, expand=YES, fill=X)

                # Iterate for each of the switches
                for top, mount, state, mode in switches:
                    TOGGLESWITCH(mframe, 
                                 mount=mount, 
                                 outside=20,
                                 nutbase=metal, 
                                 mode=mode,
                                 bg="slategray2", 
                                 top=top,
                                 status=state).frame.pack(side=LEFT, 
                                                          expand=YES,
                                                          padx=2, pady=6)

if __name__ == '__main__':
    TestSwitches().mainloop()




