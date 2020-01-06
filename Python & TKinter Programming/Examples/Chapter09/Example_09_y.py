from Common  import *
from Tkinter import *

from crilib import *
import sys, regex, serial, time

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
        keep_polling = TRUE

        try:
            line = self.fd.write('D\r')
            # OK, read the serial line (wait maximum of 1500 mSec)
            inl = self.fd.readTerminated()
            self.lfd.write('%s\n' %inl)
            return inl
        except:
            return 'XX'

class MultiMeter:
    def __init__(self, master):
        self.root = master
        self.root.title("Digital Multimeter")
        self.root.iconname('22-168a')

        self.canvas = Canvas(self.root, width=300, height=694)
        self.canvas.pack(side="top", fill=BOTH, expand='no')

        self.img = PhotoImage(file='multimeter.gif')
        self.canvas.create_image(0,0,anchor=NW, image=self.img)

        self.multimeter = MeterServer()

        self.root.after(500, self.doPoll)

    def doPoll(self):
        result = self.multimeter.poll()
        if result:
            self.updateDisplay(result)
        self.root.after(500, self.doPoll)
        
    def updateDisplay(self, result):
        self.canvas.delete('display')
        if result[:2] == 'XX':
            self.canvas.create_text(150, 100, text="Off",
                                    font=("Digiface", 72),
                                    fill="#333377",
                                    anchor = CENTER,
                                    tags="display")        
        else:
            tag   = result[:2]
            val   = result[2:8]
            units = result [9:13]
            print tag, val, units
            stro = '%s %s %s' % (tag, val, units)
            self.canvas.create_text(150, 100, text=stro,
                                    font=("Digiface", 72),
                                    fill="#333377",
                                    anchor = CENTER,
                                    tags="display")        
            
######################################################################
if __name__ == '__main__':
    root = Tk()
    multimeter = MultiMeter(root)
    multimeter.root.mainloop()
