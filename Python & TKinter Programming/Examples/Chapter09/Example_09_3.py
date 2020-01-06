from Common  import *
from Tkinter import *

import time, Utils

timeDigits = [(415, 170, 'hour[:1]'), (440, 172, 'hour[1:]'),
              (465, 174, '":"'),      (490, 176, 'min[:1]'),
              (515, 176, 'min[1:]'),  (540, 174, '":"'),
              (565, 172, 'sec[:1]'),  (590, 170, 'sec[1:]')] # [1]

setDigits  = [(185, 180, 'self.h1'), (210, 180, 'self.h2'),
              (235, 180, '":"'),     (260, 180, 'self.m1'),
              (285, 180, 'self.m2')]

SECONDS_PER_DAY = 86400

class Machine:
    def __init__(self, master):
        self.root = master
        self.root.title("Alien Machine")
        self.root.iconname('TAHL')

        self.curDigit = 0
        self.h1       = 0
        self.h2       = 0
        self.m1       = 0
        self.m2       = 0
        self.digits   = ['h1','h2','m1','m2']
        self.inSet    = FALSE
        
        self.canvas = Canvas(self.root, width=640, height=480)
        self.canvas.pack(side="top", fill=BOTH, expand='no')

        self.img = PhotoImage(file='images/machine.gif')  # [2]
        self.canvas.create_image(0,0,anchor=NW, image=self.img)

        self.b1 = self.canvas.create_oval(216,285, 270,340, fill="", 
                             outline='#226644', width=3, tags='b_1')
        # [3]
        self.canvas.tag_bind(self.b1, "<Any-Enter>", self.mouseEnter)
        self.canvas.tag_bind(self.b1, "<Any-Leave>", self.mouseLeave)

        self.b2 = self.canvas.create_oval(216,355, 270,410, fill="", 
                             outline='#772244', width=3, tags='b_2')

        self.canvas.tag_bind(self.b2, "<Any-Enter>", self.mouseEnter)
        self.canvas.tag_bind(self.b2, "<Any-Leave>", self.mouseLeave)

	Widget.bind(self.canvas, "<1>", self.mouseDown)  # [4]

        self.buttonAction = { 'b_1': self.b1_action,     # [5]
                              'b_2': self.b2_action }

    def mouseDown(self, event):
	# see if we're on a button. If we are, it
	# gets tagged as CURRENT for by Tk.              # [6]
	if event.widget.find_withtag(CURRENT):
	    tags = self.canvas.gettags('current')
	    if '_' in tags[0]:
                self.buttonAction[tags[0]]()

    def mouseEnter(self, event):
        # the CURRENT tag is applied to
        # the object the cursor is over.
	tags = self.canvas.gettags('current')
	usetag  = tags[0]
	self.lastcolor = self.canvas.itemcget(usetag, 'outline')
	self.canvas.itemconfig(usetag,  outline=Color.HIGHLIGHT)
	self.canvas.itemconfig(usetag,  fill=self.lastcolor)
	
    def mouseLeave(self, event):
	tags = self.canvas.gettags('current')
	usetag  = tags[0]
	self.canvas.itemconfig(usetag, outline=self.lastcolor)
	self.canvas.itemconfig(usetag,  fill="")

    def b1_action(self):
        if self.inSet:
            value = getattr(self, self.digits[self.curDigit])
            value = value + 1
            setattr(self, self.digits[self.curDigit], value)
            self.makeTime()
            self.displaySet()

    def b2_action(self):
        if not self.inSet:
            self.inSet = TRUE
            self.displaySet()
            self.root.after(1000, self.displayTime)
        else:
            self.curDigit = self.curDigit + 1
            if self.curDigit > 3:
                self.inSet = FALSE
                self.canvas.delete('settag')
                self.mouseLeave(None)
                self.doCountdown()
        
    def displaySet(self):
        self.canvas.delete('settag')          # [7]
        for x,y, what in setDigits:
            value = eval(what)
            self.canvas.create_text(x, y, text=value, tags="settag",
                 font=("StingerLight", 36), fill="#22AAFF")
        
    def makeTime(self):
        if self.m2 > 9:
            self.m1 = self.m1 + 1
            self.m2 = 0
        if self.m1 > 5:
            self.h2 = self.h2 + 1
            self.m1 = 0
        if self.h2 > 3 and self.h1 == 2:
            self.h2 = 0
            self.h1 = 0
        if self.h2 > 9:
            self.h2 = 0
            self.h1 = self.h1 + 1
        if self.h1 > 2:
            self.h1 = 0

    def displayTime(self):
        y,m,d,h,min,s,wday,jday,dst = time.localtime(time.time())
        self.canvas.delete('timetag')
        
        hour = str(100+h)[-2:]
        min  = str(100+min)[-2:]        
        sec  = str(100+s)[-2:]        

        for x,y, what in timeDigits:
            value = eval(what)
            self.canvas.create_text(x, y, text=value, tags="timetag",
                 font=("StingerLight", 36, "bold"), fill="#FF6666")
        self.root.after(1000, self.displayTime)            
        
    def doCountdown(self):
        hhmm = '%d%d%d%d' % (self.h1, self.h2, self.m1, self.m2)
        csec = Utils.hhmm_to_seconds(hhmm)
        tsec = Utils.hhmm_to_seconds(Utils.get_hhmm(time.time()))
        if csec > tsec:
            self.seconds = (csec - tsec) - 1
        else:
            self.seconds = ((SECONDS_PER_DAY - tsec) + csec) - 1
        self.root.after(1000, self.tick)

    def tick(self):
        self.canvas.delete('ticktag')
        self.canvas.create_text(240, 190, text=`self.seconds`,
                  font=("StingerLight", 36), fill="#44FFFF",
                  tags="ticktag", anchor=CENTER)
        self.seconds = self.seconds - 1
        if self.seconds <= 0:
            self.canvas.delete('ticktag')
            self.canvas.create_text(240,195, text=MESSAGE,
                      font=("StingerLight", 30), fill="#2288FF",
                      tags="ticktag", anchor=CENTER)
        else:
            self.root.after(1000, self.tick)

######################################################################
if __name__ == '__main__':
    root = Tk()
    machine = Machine(root)
    machine.root.mainloop()


