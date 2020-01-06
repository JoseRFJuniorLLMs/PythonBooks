from Common  import *
from Tkinter import *

from Example_09_1_data import *

from crilib import *
import sys, regex, serial, time, string, os

IGNORE   = '\n\r'

class RS232(serial.Port):
    def __init__(self):
        serial.Port.__init__(self)
        self.queryPat = regex.compile('^.*\?$')

    def open(self, cfg):
        self.debug = cfg['debug']
        self._trace('RS232.open')
        cfg['cmdsEchoed']  = FALSE
        cfg['cmdTerm']     = '\r'
        cfg['rspTerm']     = '\r'
        cfg['rspType']     = serial.RSP_TERMINATED
        serial.Port.open(self, cfg)

class MeterServer:
    def __init__(self):
        # Open up the serial port
        try:
            d = serial.PortDict()
            d['port']      = serial.COM1
            d['baud']      = serial.Baud1200
            d['parity']    = serial.NoParity
            d['dataBits']  = serial.WordLength7
            d['stopBits']  = serial.TwoStopBits
            d['timeOutMs'] = 1500
            d['rspTerm']   = IGNORE
            d['rtsSignal'] = 'C'
            d['debug']     = FALSE
            self.fd = RS232()
            self.fd.open(d)
            self.lfd = open('out.log', 'w')
        except:
            print 'Cannot open serial port (COM1)'
            sys.exit()

    def poll(self):
        try:
            line = self.fd.write('D\r')
            # OK, read the serial line (wait maximum of 1500 mSec)
            inl = self.fd.readTerminated()
            self.lfd.write('%s\n' %inl)
            return inl
        except:
            return 'XX   Off     '

class MultiMeter:
    def __init__(self, master):
        self.root = master
        self.root.title("Digital Multimeter")
        self.root.iconname('22-168a')

        self.holdVal  = '0.0'
        self.curRange = None
        self.lineOpen = FALSE

        self.canvas = Canvas(self.root, width=300, height=694)
        self.canvas.pack(side="top", fill=BOTH, expand='no')

        self.img = PhotoImage(file='images/multimeter.gif')
        self.canvas.create_image(0,0,anchor=NW, image=self.img)

        self.buildScale()

        self.root.update()
        self.root.after(5, self.buildSymbols)
        self.dataReady = FALSE
        self.root.after(5, self.buildScanner)

        self.multimeter = MeterServer()
        self.root.after(500, self.doPoll)

    def buildSymbols(self):
        for x, y, font, txt, tag in PANEL_LABELS:
            self.canvas.create_text(x, y, text=txt,
                                    font=(font, 12),
                                    fill="gray75",
                                    anchor = CENTER,
                                    tags=tag)        

    def buildScale(self):
        self.canvas.create_line(75,150, 213,150,
                                width=1,fill="#333377")
        self.Xincr = 140.0/40.0
        self.X  = x = 75
        self.X1 = 213
        y = 150
        lbli = 0
        for i in range(40):
            lbl = ''
            if i in [0,9,19,29,39]:
                h    = 6
                lbl  = `lbli`
                lbli = lbli + 5
            elif i in [5,14,24,34]:
                h = 4
            else:
                h = 2
            self.canvas.create_line(x,y, x,y-h,
                                width=1,fill="#333377")
            if lbl:
                self.canvas.create_text(x, y-5, text=lbl,
                                        font=("Arial", 6),
                                        fill="#333377",
                                        anchor = S),
            x = x + self.Xincr
            
    def startAnimation(self):
        self.animX = self.X
        self.action = TRUE
        self.root.after(30, self.animate)
        
    def animate(self):
        if self.action:
            self.canvas.create_line(self.animX,155, self.animX,167,
                                    width=2,fill="#333377",
                                    tags='anim')
            self.animX = self.animX + self.Xincr
            if self.animX > self.X1:
                self.animX= self.X
                self.canvas.delete('anim')
            self.root.after(30, self.animate)
        else:
            self.canvas.delete('anim')
            
    def stopAnimation(self):
        self.action = FALSE
        
    def buildScanner(self):
        self.primary_lookup = {}
        for key, hasr, rfmt, un, sec in PRIMARY_DATA:
            if not self.primary_lookup.has_key(key):
                self.primary_lookup[key] = []
            self.primary_lookup[key].append((hasr, rfmt, un, sec))

        keys = SECONDARY_DATA.keys()
        for key in keys:
            img = SECONDARY_DATA[key][-2]
            try:
                if getattr(self, 'i%s' % key):
                    pass    # Already done...
            except:
                setattr(self, 'i%s' % key,
                        PhotoImage(file="images/%s.gif" % img))
        self.dataReady = TRUE
        
    def doPoll(self):
        if self.dataReady:
            result = self.multimeter.poll()
            if result:
                self.updateDisplay(result)
        self.root.after(1000, self.doPoll)
        
    def getRange(self, tag, val, units):
        matchlist = self.primary_lookup[tag]       
        if not matchlist: return None
        gotIndex = None
        gotOpenLine = FALSE
        for hasr, rfmt, un, sec in matchlist:
            if hasr and (string.find(val, 'L') >= 0):
                if rfmt == string.strip(val):
                    gotIndex = sec
                    gotOpenLine = TRUE
            else:
                decimal = string.find(val, '.')
                if decimal > 0:
                    if rfmt == `decimal`:
                        gotIndex = sec
                else:
                    if not rfmt:  # No decimals
                        gotIndex = sec
            if gotIndex:
                if not string.strip(units) == string.strip(un):
                    gotIndex = None
            if gotIndex:
                break
        return (gotIndex, gotOpenLine)

    def updateDisplay(self, result):
        self.canvas.delete('display')
        tag   = result[:2] 
        val   = result[3:9]
        units = result [9:13]

        # display the hold value
        redraw = FALSE
        try:
            hold = string.atof(self.holdVal)
            nval = string.atof(val)
            if hold <= 0.0:
                if nval < 0.0:
                    if nval < hold:
                        self.holdVal = val
                        redraw = TRUE
                else:
                    hold = 0.0
            if hold >= 0.0 and not redraw:
                if nval >= 0.0:
                    if nval > hold:
                        self.holdVal = val
                        redraw = TRUE
                else:
                    self.holdVal = '0.0'
                    redraw = TRUE
        except ValueError:
            self.holdVal = '0.0'
            redraw = TRUE
        if redraw:
            self.canvas.delete('holdval')
            self.canvas.create_text(263, 67, text=self.holdVal,
                                    font=("Digiface", 16),
                                    fill="#333377",
                                    anchor = E,
                                    tags="holdval")
        
        range, openline = self.getRange(tag, val, units)
        if range:    # Change the control to reflect the range
            if not self.curRange == range:
                self.curRange = range
                self.canvas.delete('control')
                self.canvas.create_image(146, 441, anchor=CENTER,
                     image=getattr(self, 'i%s' % range), tags="control")
                self.holdVal = '0.0'  # reset

            if openline:
                self.startAnimation()
            else:
                self.stopAnimation()
                    
            # Now we will update the units symbols pn the display
            ma,ua,a,mv,v,ko,mo,o,nf,uf,f,mhz,khz,hz,ac, ctrl, lbl = \
                SECONDARY_DATA[range]                                   
            for tag in ['ma','ua','a','mv','v','ko','mo','o',
                        'nf','uf','f','mhz','khz','hz','ac']:
	        self.canvas.itemconfig(tag,
                         fill=['gray75','#333377'][eval(tag)])

                # Update the label field if there is one
                self.canvas.delete('label') 
                if lbl:
                    self.canvas.create_text(55, 150, text=lbl,
                                font=("Arial", 12),
                                fill="#333377",
                                anchor = CENTER,
                                tags="label")        
                
        # Finally, display the value
        self.canvas.create_text(214, 100, text=val,
                                font=("Digiface", 48),
                                fill="#333377",
                                anchor = E,
                                tags="display")        

######################################################################
if __name__ == '__main__':
    root = Tk()
    multimeter = MultiMeter(root)
    multimeter.root.mainloop()

