# 
#  GUI Common Class definitions
#

from Common_7_1 import *

class GUICommon:
    def turnon(self):
        self.status = STATUS_ON
        if not self.blink: self.update()

    def turnoff(self):
        self.status = STATUS_OFF
        if not self.blink: self.update()

    def alarm(self):
        self.status = STATUS_ALARM
        if not self.blink: self.update()

    def warn(self):
        self.status = STATUS_WARN
        if not self.blink: self.update()

    def set(self, color):
        self.status       = STATUS_SET
        self.specialColor = color
        self.update()

    def blinkon(self):
        if not self.blink:
            self.blink   = 1
            self.onState = self.status
            self.update()

    def blinkoff(self):
        if self.blink:
            self.blink   = 0
            self.status  = self.onState
            self.onState = None
            self.on=0
            self.update()

    def blinkstate(self, blinkstate):
        if blinkstate:
            self.blinkon()
        else:
            self.blinkoff()

# This routine modifies an RGB color (returned by winfo_rgb),
# applys a factor, maps -1 < Color < 255 and returns new RGB string

    def transform(self, rgb, factor):
        retval = "#"
        for v in [rgb[0], rgb[1], rgb[2]]:
	    v = (v*factor)/256
            if v > 255: v = 255
            if v < 0:   v = 0
            retval = "%s%02x" % (retval, v)
        return retval

# This routine factors dark, very dark, light and very light colors
# from the base color using transform

    def set_colors(self):
        rgb = self.winfo_rgb(self.base)
        self.dbase  = self.transform(rgb, 0.8)
        self.vdbase = self.transform(rgb, 0.7)
        self.lbase  = self.transform(rgb, 1.1)
        self.vlbase = self.transform(rgb, 1.3)

# The following define drawing vertices for various 
# graphical elements

ARROW_HEAD_VERTICES = [
     ['x-d', 'y-d', 'x',   'y+d', 'x+d', 'y-d', 'x-d', 'y-d'],
     ['x',   'y-d', 'x-d', 'y+d', 'x+d', 'y+d', 'x',   'y-d'],
     ['x-d', 'y-d', 'x+d', 'y',   'x-d', 'y+d', 'x-d', 'y-d'],
     ['x-d', 'y',   'x+d', 'y+d', 'x+d', 'y-d', 'x-d', 'y'  ]]

