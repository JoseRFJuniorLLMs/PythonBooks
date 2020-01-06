from Tkinter import *
from ftplib import *
import Pmw
import string, time, os
import thread

from testdata import testData

####################################################################
# Constants
####################################################################

TEMP  = 1
PRESS = 2
SPEED = 3
HUM   = 4
VISIB = 5
DIR   = 6
CLOW  = 7
CHGH  = 8

BLANK_VALUE = -123321

noaa_url  = "weather.noaa.gov"
metar_dir = "/data/observations/metar/stations/"
temp_dir  = "/Temp"

digits = '0123456789'

####################################################################
# Weather Monitor
####################################################################

class WeatherMonitor:
    def __init__(self, master=None, host='', width=900, height=600,
                 bd=1, indent=30, titlespace=20):

	self.cells = [
          (0,0,1, 'Temp', -10, 110, TEMP, ['Temp'], 'Degrees F',
           [-10,0,10,20,30,40,50,60,70,80,90,100]),
          (1,0,1, 'Pressure', 27, 32, PRESS, ['Press'],'Inches Hg.',
           [27,28,29,30,31,32]),
          (2,0,0.4, 'Wind Speed', 0, 100, SPEED, ['WSpeed'], 'MPH',
           [0,20,40,60,80,100]),
          (2,0.48,0.40,'Wind Direction', 0, 360, DIR, ['WDir'], 'Degrees',
           [0,90,180,270,360]),
          (0,1,1, 'Humidity', 0, 100, HUM, ['Humidity'],  'Percent',
           [0,20,40,60,80,100]), 
          (1,1,1, 'Visibility', 0, 50, VISIB,['Visibility'], 'Miles',
           [0,10,20,30,40,50]), 
          (2,1,0.40, 'Cloud High', 10, 100, CHGH, ['CHigh', 'CVHigh'],
              'Feet (K)',
           [10,25,50,75,100]),
          (2,1.48,0.40, 'Cloud Low', 0, 30, CLOW, ['CLow'], 'Feet (K)',
           [0,5,10,15,20,25])
          ]

	self.XAxisData = {
            '5 Minutes':     ([0,1,2,3,4,5], 'Min'), 
            '10 Minutes':    ([0,2,4,6,8,10], 'Min'),
            '30 Minutes':    ([0,5,10,15,20,25,30], 'Min'), 
            '1 Hour':        ([0,10,20,30,40,50,60], 'Min'),
            '12 Hours':      ([0,2,4,6,8,10,12], 'Hrs'),
            '24 Hours':      ([0,4,8,12,16,20,24], 'Hrs')
                         }

	self.usePoll        = []
	self.Sessions       = {}
	self.wStation       = 'KPVD'

	self.Surround       = 'Gray10'
	self.Base           = 'Gray80'
        self.Graph          = 'Gray20'
	self.Line           = '#22ffdc'
	self.Axes           = 'MediumSeaGreen'
	self.Labels         = 'MediumSeaGreen'
	self.Titles         = 'DarkGoldenRod1'
	self.CrossHairsH    = '#006600'
	self.CrossHairsV    = '#008800'

	self.master        = master
	self.indent        = indent
	self.titlespace    = titlespace
	self.xindent       = (indent/4)*3
	self.yindent       = indent/4
	self.width         = width+(3*indent)
	self.height        = height+(2*indent)+(2*titlespace)
	self.cellWidth     = self.width/3
	self.cellHeight    = self.height/2
	self.axisWidth     = self.cellWidth - self.indent
	self.axisHeight    = self.cellHeight - \
                             (self.indent+self.titlespace)
	self.displayItems  = '12 Hours'
	self.refreshRate   = 60
	self.plottedData   = 'PMMarker'

        self.gotData       = FALSE
        self.threadRunning = FALSE
        self.testIndex     = 0

	self.frame=Frame(master, height=self.height,
                         width=self.width, relief='raised',
                         bd=bd)
	self.frame.pack(fill=BOTH, expand=0)
	self.innerframe=Frame(master, height=40, width=self.width,
                              relief='raised',
                              bg=self.Base, bd=bd)
	self.innerframe.pack(side=BOTTOM, fill=X, expand=0)
	self.refresh=Pmw.ComboBox(self.innerframe,
             history=0,
             entry_state = 'disabled', labelpos = W,
             label_text = 'Refresh Rate:',
             selectioncommand = self.setDisplayRate,
	     scrolledlist_items=('Default','1 Minute','5 Minutes',
                                 '10 Minutes','30 Minutes'))
	self.refresh.pack(padx=3, pady=3, side=LEFT)
	self.refresh.selectitem('Default')
	self.selector=Pmw.ComboBox(self.innerframe,
	     entry_state = 'disabled', history=0,
	     label_text = 'Display:', labelpos = W,
             selectioncommand = self.setDisplayRange,
	     scrolledlist_items=('10 Minutes','30 Minutes','1 Hour',
                                 '12 Hours','24 Hours'))
	self.selector.pack(padx=3, pady=3, side=LEFT)
	self.selector.selectitem('12 Hours')
	self.station=Pmw.ComboBox(self.innerframe,
             entry_state = 'disabled',
             history=0, label_text = 'Station:', labelpos = W,
             selectioncommand = self.setStation)
	self.station.pack(padx=3, pady=3, side=LEFT)

        fd = open('stations.txt')
        dataIn = fd.readlines()
        fd.close()
        stationList = []
        for data in dataIn:
            stationList.append(data[:-1])   # remove trailing newline
        self.station.setlist(stationList)
        self.station.selectitem('KPVD Providence')

	self.canvas=Canvas(self.frame, width=self.width,
             highlightthickness=0, height=self.height, bg=self.Surround)
	self.canvas.pack(side="top", fill='x', expand='no')

	self.canvas.create_line(0,self.cellHeight,self.width+1,
                                self.cellHeight,
				fill='gray40', width=2)
	self.canvas.create_line(self.cellWidth+1,0,self.cellWidth+1,
                                self.height+1,
				fill='gray40', width=2)
	self.canvas.create_line((2*self.cellWidth)+1,0,
                                (2*self.cellWidth)+1,self.height+1,
				fill='gray40', width=2)

	self.maxSpan          = None

	self.pollTime         = None  # Time for these data

        self.Temp             = None
        self.Press            = None
        self.WSpeed           = None
        self.Humidity         = None
        self.Visibility       = None
        self.WDir             = None
        self.CLow             = None
        self.CHigh            = None        
        self.CVHigh           = None        
        
        self.lastTemp         = (-999.0,-999.0)
        self.lastPress        = (-999.0,-999.0)
        self.lastWSpeed       = (-999.0,-999.0)
        self.lastHumidity     = (-999.0,-999.0)
        self.lastVisibility   = (-999.0,-999.0)
        self.lastWDir         = (-999.0,-999.0)
        self.lastCLow         = (-999.0,-999.0)
        self.lastCHigh        = (-999.0,-999.0)        
        self.lastCVHigh       = (-999.0,-999.0)        

        self.setup_plot()

    def setup_plot(self, restart=1):
	for xf, yf, af, label, low, high, dataType, datalist, \
                yAxisLabel, ticklist in self.cells:
	    x0=(self.cellWidth*xf)+self.xindent
	    x1=(self.cellWidth*xf)+self.xindent+self.axisWidth
	    y0=(self.cellHeight*yf)+self.yindent+self.titlespace+1
	    y1=(self.cellHeight*yf)+self.yindent+self.titlespace+\
                (self.axisHeight*af)+1
	    self.canvas.create_rectangle(x0,y0,x1,y1,
					 fill=self.Graph, outline="")
	    self.canvas.create_line(x0,y0,x0,y1,
				    fill=self.Axes, width=2)
            if low <= 0:
                spread=abs(low)+abs(high)
                yx=float((spread-abs(low)))/float(spread)*\
                    (self.axisHeight*af)+y0
                self.canvas.create_line(x0,yx,x1,yx,
                                        fill=self.Axes, width=2)

	    self.canvas.create_text(x1-2,y0-self.titlespace+2,
                               text=label, font=('Verdana', 12),
                               fill=self.Titles,anchor='ne')
	    self.canvas.create_text(x0+2,y0-self.titlespace+2,
                               text=yAxisLabel, font=('Verdana', 12),
                               fill=self.Titles,anchor='nw')

	    self.doYAxis(x0, x1, y0, af, low, high, ticklist)
	    self.doXAxis(x0, x1, y0, y1, label)
	    self.canvas.create_line(x0,y0,x1,y0,
				    fill=self.Axes, width=2)
	    self.canvas.create_line(x1,y0,x1,y1,
				    fill=self.Axes, width=2)
	    self.canvas.create_line(x0,y1,x1,y1,
				    fill=self.Axes, width=2)

	self.baseTime         = time.time()
	self.setDisplayRange(self.displayItems)

	if restart:
	    self.doPlot()

    def doYAxis(self, x0, x1, y0, af, low, high, ticklist):
        if low <= 0:
            spread=abs(low)+abs(high)
        else:
            spread = high-low
	negcomp=self.calculate_negative_component(low, high)
	for tick in ticklist:
            tickV = tick
            tickL = `tick`
	    y=((float(spread-(tickV+negcomp))/float(spread))*\
               (self.axisHeight*af))+y0-1
	    self.canvas.create_text(x0-2,y, text=tickL,
                                    font=('Verdana', 8),
                                    fill=self.Axes, anchor='e')
	    if not tickV == 0:
	        self.canvas.create_line(x0,y,x0+4,y, fill=self.Axes,
                                        width=2)
		self.canvas.create_line(x0+4,y,x1,y,
                                       fill=self.CrossHairsH, width=1)

    def doXAxis(self, x0, x1, y0, y1, tag):
	intlist, label = self.XAxisData[self.displayItems]
	ltag = translate_spaces(tag,'_')
	self.canvas.delete(ltag)   # Remove previous scales
	incr = self.axisWidth / (len(intlist)-1)
	xt = x0
	for tick in intlist:
	    if xt > x0:
	        self.canvas.create_line(xt,y1,xt,y1-4,
                                        fill=self.Axes, width=2,
                                        tags=ltag)
		self.canvas.create_line(xt,y0,xt,y1-4,
                                        fill=self.CrossHairsV,
                                        width=1, tags=ltag)
	    self.canvas.create_text(xt,y1+5, text=tick,
                                    font=('Verdana', 8),
                                    fill=self.Axes, anchor='n',
                                    tags=ltag)
	    xt = xt + incr
	self.canvas.create_text(xt-(incr*2)+(incr/2),y1+2,
                                text=label, font=('Verdana', 12),
                                fill=self.Titles, anchor='n',
                                tags=ltag)

    def doPlot(self):
        if self.gotData:
            self.gotData       = FALSE
            self.threadRunning = FALSE
        else:
            if self.threadRunning:
                self.frame.after(1000, self.doPlot)   # Spin for changes
                return
            else:
                self.threadRunning = TRUE
                self.gotData       = FALSE
                thread.start_new(self.getMETAR, (noaa_url,metar_dir,
                                                 self.wStation))
                self.frame.after(1000, self.doPlot)   # Spin for data
                return

        if self.report:
            self.decodeMETAR(self.report)
        self.pollTime = time.time()

	for xf, yf, af, label, low, high, dataType, datalist, yAxisLabel, \
                ticklist in self.cells:
	    x0=(self.cellWidth*xf)+self.xindent
	    x1=(self.cellWidth*xf)+self.xindent+self.axisWidth
	    y0=(self.cellHeight*yf)+self.yindent+self.titlespace+1
	    y1=(self.cellHeight*yf)+self.yindent+self.titlespace+\
                (self.axisHeight*af)+1
            if low <= 0:
                spread=abs(low)+abs(high)
            else:
                spread = high-low
	    negcomp=self.calculate_negative_component(low, high)

	    for data in datalist:
		dataPoint = getattr(self, '%s' % data)
		if dataPoint or dataPoint == 0.0:
		    if self.pollTime > self.maxSpan:
			self.canvas.delete(self.plottedData) # Remove previous
			self.baseTime = self.pollTime
			self.setDisplayRange(self.displayItems)
		    xfactor = float(self.axisWidth) / (self.maxSpan - \
                                                       self.baseTime)
		    xv = self.pollTime - self.baseTime
		    if not dataPoint == float(BLANK_VALUE):
			centerx = x0 + ((xv * xfactor)-1) +2
			centery=((float(spread-(dataPoint+negcomp))/ \
                                  float(spread))*(self.axisHeight*af))+y0-1

			lastX, lastY = getattr(self, 'last%s' % data)
			if not lastY == -999.0:
			    if not lastX >= centerx:
			        self.canvas.create_line(lastX,lastY,centerx,
                                       centery,fill=self.Line,width=2,
                                                        tags=self.plottedData)
			pstr = 'self.last%s = (%d,%d)' % (data,centerx,centery)
		    else:
			pstr = 'self.last%s = (-999.0,-999.0)' % data
		else:
		    pstr = 'self.last%s = (-999.0,-999.0)' % data

		exec(pstr)

	drawinterval = 1000*self.refreshRate
	self.frame.after(drawinterval, self.doPlot)

    def setDisplayRange(self, display):
	doSetup = FALSE
	if not self.displayItems == display:
	    doSetup = TRUE
	self.displayItems = display
	[value, units] = string.splitfields(display, ' ')
	mult = 1
	if units[:1] == 'M':
	    mult = 60
	if units[:1] == 'H':
	    mult = 3600
	self.maxSpan  = self.baseTime + (string.atoi(value) * mult)
	self.canvas.delete(self.plottedData)   # Remove previous data...
	if doSetup:
            self.setup_plot(restart=0)

    def setDisplayRate(self, rate):
	newRate = 10
	if not rate == 'Default':
	    [value, units] = string.splitfields(rate, ' ')
	    mult = 1
	    if units[:1] == 'M':
		mult = 60
	    newRate = string.atoi(value) * mult
	self.set_refreshRate(newRate)
	self.baseTime      = time.time()
	self.setDisplayRange(self.displayItems)

    def setStation(self, station):
        self.wStation = station[:4]
        self.master.title("Weather Monitor (%s)" % self.wStation)
        
    def calculate_negative_component(self, low, high):
	if low < 0:
            negcomp = abs(low)
	elif low > 0:
	    negcomp = -low
        else: 
	    negcomp = low
	return negcomp

    def set_refreshRate(self, rate):
	self.refreshRate = rate

    def getMETAR(self, url=noaa_url, directory=metar_dir,
                 station='KPVD'):

##       UNCOMMENT the next line to inject test data (saves net bandwidth!)
##         return self.getTestData()

        tmp = '%s/wtemp' % temp_dir

        if os.path.exists(tmp) == 1:
            os.remove(tmp)

        data = open(tmp,'w')

        try:
            ftp = FTP(url)
            ftp.login()            
            ftp.cwd(directory)
            ftp.retrbinary('RETR %s.TXT' % station, data.write)
            ftp.quit
        except:
            print 'FTP failed...'
               
        data.close()

        report = open(tmp, 'r')
        self.report = report.read()
        self.gotData = TRUE
        
    def decodeMETAR(self, report):
        self.Temp             = None
        self.Press            = None
        self.WSpeed           = None
        self.Humidity         = None
        self.Visibility       = None
        self.WDir             = None
        self.CLow             = None
        self.CHigh            = None

        station = dtime = wind = visib = runway = weather = temp = alt = '--'
        lines = string.split(report, '\n')
        data  = string.split(lines[1], ' ')
        station  = data[0]
        dtime    = data[1]
        if not data[2][0] in 'CSA':    # COR, AUTO, SPEC
            wind = data[2]
            next = 3
        else:
            wind = data[3]
            next = 4
        if data[next][-2:] == 'SM':
            visib    = data[next]
        else:
            next = next + 1  #SKIP
            visib    = data[next]
        next     = next + 1
        if data[next][0] == 'R':
            runway = data[next]
            next = next + 1
        if data[next][:2] in ['MI','BC','PR','TS','BL','SH','DR','FZ','DZ',
                              'IC','UP','RA','PE','SN','GR','SG','GS','BR',
                              'SA','FG','HZ','FU','PY','VA','DU','SQ','FC',
                              'SS','DS','PO']:
            weather = data[next]
            next    = next + 1
        cloud = []
        while 1:
            if data[next][:3] in ['SKC','SCT','FEW','BKN','OVC','TCC','CLR']:
                cloud.append(data[next])
                next = next + 1
            else:
                break

        temp = data[next]
        next = next + 1
        alt  = data[next]

        if not wind[:3] == 'VRB':
            self.WDir   = atoi(wind[:3])
        self.WSpeed     = atoi(wind[3:])*23.0/20.0
        if self.WDir == 0 and self.WSpeed == 0.0:
            self.WDir   = None    # Calm
            self.WSpeed = 0.0

        if len(cloud) == 1 or len(cloud) == 2 or len(cloud) == 3:
            if cloud[0] == 'CLR':
                self.CLow = None
            else:
                self.CLow = atoi(cloud[0][3:6])/10
        if len(cloud) == 2 or len(cloud) == 3:
            if cloud[1] == 'CLR':
                self.CLow = None
            else:
                self.CHigh = atoi(cloud[1][3:6])/10
        elif len(cloud) == 3:
            if cloud[2] == 'CLR':
                self.CLow = None
            else:
                self.CVHigh = atoi(cloud[2][3:6])/10
            
        self.Visibility = atoi(visib)
        t, dpC          = string.split(temp, '/')
        self.Temp       = (atoi(t)*(9.0/5.0))+32
        dpF             = (atoi(dpC)*(9.0/5.0))+32
        self.Humidity   = (dpF/self.Temp)*100
        self.Press      = eval('%s.%s' % (alt[1:3], alt[-2:]), _safe_env)
           
    def getTestData(self):
        try:
            retData = 'Date Time\n%s' % testData[self.testIndex]
            self.testIndex = self.testIndex + 1
        except IndexError:
            retData = None
            self.testIndex = 0
        return retData

def translate_spaces(instring, trans):
    res = ''
    for c in instring:
	if c == ' ' or c == '\t':
	    if trans != "":   #To remove spaces
		res = res + trans
	else:
	    res = res + c
    return (res)

def translate_underbars(instring):
    res = ''
    for c in instring:
	if c == '_':
	    res = res + ' '
	else:
	    res = res + c
    return (res)

# "Safe" environment for eval()
_safe_env = {"__builtins__": {}}

def atoi(strIn):
    result = 0
    s    = string.strip(strIn)
    sign = ''
    if s:
        if s[0] in '+-':
            sign = s[0]
            s = s[1:]
	while s[0] == '0' and len(s) > 1: s = s[1:]
        str = sign
	for c in s:
            if c not in digits:
                break   #  Got a terminator
            str = str + c
        if str:
            result = eval(str, _safe_env)
    return result

if __name__ == '__main__':

    root = Tk()
    root.option_add('*background', 'grey')
    root.option_add('*foreground', 'black')
    root.option_add('*Entry.background', 'white')
    root.option_add('*Label.background', 'grey')
    Pmw.initialise(root, fontScheme = 'pmw1', useTkOptionDb = 0)
    w = WeatherMonitor(root, width=720, height=430)
    w.master.title("Weather Monitor (%s)" % w.wStation)
    w.master.iconname('Weather')
    w.master.geometry('+20+80')
    
    root.mainloop()
