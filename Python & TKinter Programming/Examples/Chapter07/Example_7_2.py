from Tkinter          import *
from Common_7_1       import *                               # <<1>>
from GUICommon_7_1    import *                               # <<2>>

class LED(GUICommon):                                         # <<3>>
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
        self.Colors       = [None, Color.OFF, Color.ON,       # <<4>> 
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
                               highlightthickness=0, bg=bg, bd=0)
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
                               highlightthickness=0, bg=bg, bd=0)
            x = d
            y = d
                                                              # <<5>>
            VL = ARROW_HEAD_VERTICES[orient] # Get the vertices for the arrow
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

        # Set color for current status                        # <<6>>
        self.canvas.itemconfig(self.light, fill=self.Colors[self.status])

        self.canvas.update_idletasks()

        if self.blink:
            self.frame.after(self.blinkrate * 1000, self.update)

if __name__ == '__main__':
    class TestLEDs(Frame):
        def __init__(self, parent=None):

            # List of Colors and Blink On/Off
            states = [(STATUS_OFF,   0),     
                      (STATUS_ON,    0),
                      (STATUS_WARN,  0),
                      (STATUS_ALARM, 0),
                      (STATUS_SET,   0),
                      (STATUS_ON,    1),
                      (STATUS_WARN,  1),
                      (STATUS_ALARM, 1),
                      (STATUS_SET,   1)]

            # List of LED types to display,
            # with sizes and other attributes
            leds = [(ROUND,  15, 15, FLAT,   0, None,        "gray50"),
                    (ROUND,  15, 15, RAISED, 1, None,        ""),
                    (SQUARE, 12, 12, SUNKEN, 1, None,        ""),
                    (SQUARE,  8,  8, FLAT,   0, None,        ""),
                    (SQUARE,  8,  8, RAISED, 0, None,        ""),
                    (SQUARE, 16,  8, FLAT,   1, None,        ""),
                    (ARROW,  14, 14, RIDGE,  1, POINT_UP,    ""),
                    (ARROW,  14, 14, RIDGE,  0, POINT_LEFT,  "black"),
                    (ARROW,  14, 14, FLAT,   0, POINT_DOWN,  "yellow")]

            Frame.__init__(self)              # Do superclass init
            self.pack()
            self.master.title('LED - Stage 2')  # Label Toplevel shell

            # Iterate for each type of led
            for shape, w, h, app, bd, orient, outline in leds:
                frame = Frame(self, bg=Color.PANEL)
                frame.pack(anchor=N, expand=YES, fill=X)

                # Iterate for selectes states
                for state, blink in states:
                    LED(frame, shape=shape, status=state,
                        width=w, height=h, appearance=app,
                        orient=orient, blink=blink, bd=bd, 
                        outline=outline).frame.pack(side=LEFT,
                                                    expand=YES,
                                                    padx=1, pady=1)

TestLEDs().mainloop()


