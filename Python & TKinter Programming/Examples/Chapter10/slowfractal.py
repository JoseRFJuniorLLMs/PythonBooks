from   Tkinter import *
import Pmw
import AppShell

DISTANCE   = 0
ITERATIONS = 1

import cmath
import math

_PI = cmath.pi
_TWO_PI = _PI * 2
_THIRD_PI = _PI / 3
_SIXTH_PI = _PI / 6

def rgb2name(rgb):
    return '#%02x%02x%02x' % \
        (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

def hsi2rgb(hue, saturation, intensity):
    i = intensity
    if saturation == 0:
	rgb = [i, i, i]
    else:
	hue = hue / _THIRD_PI
	f = hue - math.floor(hue)
	p = i * (1.0 - saturation)
	q = i * (1.0 - saturation * f)
	t = i * (1.0 - saturation * (1.0 - f))

	hue = int(hue)
	if   hue == 0: rgb = [i, t, p]
	elif hue == 1: rgb = [q, i, p]
	elif hue == 2: rgb = [p, i, t]
	elif hue == 3: rgb = [p, q, i]
	elif hue == 4: rgb = [t, p, i]
	elif hue == 5: rgb = [i, p, q]

    for index in range(3):
	val = rgb[index]
	if val < 0.0:
	    val = 0.0
	if val > 1.0:
	    val = 1.0
	rgb[index] = val

    return rgb

def correct(rgb, correction):
    correction = float(correction)
    rtn = []
    for index in range(3):
	rtn.append((1 - (1 - rgb[index]) ** correction) ** (1 / correction))
    return rtn

def spectrum(numColors, correction = 1.0, saturation = 1.0, intensity = 1.0,
	extraOrange = 1, returnHues = 0):
    colorList = []
    division = numColors / 7.0
    for index in range(numColors):
	if extraOrange:
	    if index < 2 * division:
		hue = index / division
	    else:
		hue = 2 + 2 * (index - 2 * division) / division
	    hue = hue * _SIXTH_PI
	else:
	    hue = index * _TWO_PI / numColors
	if returnHues:
	    colorList.append(hue)
	else:
	    rgb = hsi2rgb(hue, saturation, intensity)
	    if correction != 1.0:
		rgb = correct(rgb, correction)
	    name = rgb2name(rgb)
	    colorList.append(name)
    return colorList

class Fractal(AppShell.AppShell):
    usecommandarea = 1
    appname        = 'Fractal Demonstration'        
    frameWidth     = 1000
    frameHeight    = 720
    
    def createButtons(self):
        self.buttonAdd('Save',
              helpMessage='Save current data',
              statusMessage='Write current information to database',
              command=self.save)
        self.buttonAdd('Close',
              helpMessage='Close Screen',
              statusMessage='Exit',
               command=self.close)
        
    def createCanvas(self):
        self.form = self.createcomponent('form', (), None,
                                         Frame, (self.interior(),),)
        self.form.pack(side=TOP, expand=YES, fill=BOTH)
        self.width  = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.canvas = self.createcomponent('canvas', (), None,
                                           Canvas, (self.form,),
                                           width=self.width,
                                           height=self.height)
        self.canvas.pack()
        
    def initData(self):
        self.depth       = 20
        self.origin      = -1.4+1.0j
        self.range       = 4.0
        self.maxDistance = 20.0
        self.coloration  = DISTANCE
        self.ncolors     = 64
        self.palette     = spectrum(self.ncolors)
        self.pixmap      = None
        
    def createImage(self):
        for y in range(self.height):
            for x in range(self.width):
                z = complex(0.0, 0.0)
                k = complex(self.origin.real + \
                            float(x)/float(self.width)*self.range,
                            self.origin.imag - \
                            float(y) / float(self.height)*self.range)

                # calculate z = z * z + k over and over

                for iteration in range(self.depth):
                    real = z.real
                    z = complex(z.real * z.real - z.imag * z.imag + k.real,
                                2 * real + z.imag + k.imag)

                    distance = int(z.real * z.real + z.imag * z.imag)

                    if distance >= self.maxDistance:
                        if self.coloration == DISTANCE:
                            color = self.palette[distance % self.ncolors]
                        else:
                            color = self.palette[iteration % self.ncolors]                            
                        self.pixel(x, y, color)
                        self.root.update()
                        break
                    
    def pixel(self, x, y, color):
        self.canvas.create_line(x, y, x+1, y+1, width=1, fill=color)

    def save(self):
        pass

    def close(self):
        self.quit()

    def createInterface(self):
        AppShell.AppShell.createInterface(self)
        self.createButtons()
        self.createCanvas()
        self.initData()
        self.createImage()
        
if __name__ == '__main__':
    fractal = Fractal()
    fractal.run()



