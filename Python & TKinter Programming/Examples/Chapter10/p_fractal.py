from   Tkinter import *
import Pmw, AppShell, Image, ImageDraw, os

class Palette:
    def __init__(self):
        self.palette = [(0,0,0), (255,255,255)]

    def getpalette(self):
        # flatten the  palette
        palette = []
        for r, g, b in self.palette:
            palette = palette + [r, g, b]
        return palette

    def loadpalette(self, cells):
	import random 
        for i in range(cells-2):
            self.palette.append((
                random.choice(range(0, 255)),  # red
                random.choice(range(0, 255)),  # green           
                random.choice(range(0, 255)))) # blue

class Fractal(AppShell.AppShell):
    usecommandarea = 1
    appname        = 'Fractal Demonstration'        
    frameWidth     = 780
    frameHeight    = 580
    
    def createButtons(self):
        self.buttonAdd('Save',
              helpMessage='Save current image',
              statusMessage='Write current image as "out.gif"',
              command=self.save)
        self.buttonAdd('Close',
              helpMessage='Close Screen',
              statusMessage='Exit',
               command=self.close)
        
    def createDisplay(self):
        self.width  = self.root.winfo_width()-10
        self.height = self.root.winfo_height()-95
        self.form = self.createcomponent('form', (), None,
                                         Frame, (self.interior(),),
                                         width=self.width,
                                         height=self.height)
        self.form.pack(side=TOP, expand=YES, fill=BOTH)
        self.im = Image.new("P", (self.width, self.height), 0)

        self.d = ImageDraw.ImageDraw(self.im)
        self.d.setfill(0) 
        self.label = self.createcomponent('label', (), None,
                                           Label, (self.form,),)
        self.label.pack()
        
    def initData(self):
        self.depth       = 20
        self.origin      = complex(-1.4, 1.0)
        self.range       = 2.0
        self.maxDistance = 4.0
        self.ncolors     = 256
        self.rgb         = Palette()
        self.rgb.loadpalette(255)
        self.save        = FALSE
        
    def createImage(self):
        self.updateProgress(0, self.height)
        for y in range(self.height):
            for x in range(self.width):
                z = complex(0.0, 0.0)
                k = complex(self.origin.real + \
                            float(x)/float(self.width)*self.range,
                            self.origin.imag - \
                            float(y) / float(self.height)*self.range)

                # calculate z = (z +k) * (z + k) over and over

                for iteration in range(self.depth):
                    real_part = z.real + k.real
                    imag_part = z.imag + k.imag
		    del z
                    z = complex(real_part * real_part - imag_part * \
                                imag_part, 2 * real_part * imag_part)
                    distance  = z.real * z.real + z.imag * z.imag

                    if distance >= self.maxDistance:
			cidx = int(distance % self.ncolors)
                        self.pixel(x, y, cidx)
                        break
            self.updateProgress(y)
        self.updateProgress(self.height, self.height)
        self.im.putpalette(self.rgb.getpalette())
        self.im.save("out.gif")
        self.img = PhotoImage(file="out.gif")
        self.label['image'] = self.img
            
    def pixel(self, x, y, color):
        self.d.setink(color)
        self.d.point((x, y))

    def save(self):
        self.save = TRUE
        self.updateMessageBar('Saved as "out.gif"')

    def close(self):
        if not self.save:
            os.unlink("out.gif")
        self.quit()

    def createInterface(self):
        AppShell.AppShell.createInterface(self)
        self.createButtons()
        self.initData()
        self.createDisplay()
        
if __name__ == '__main__':
    def start():
        fractal = Fractal()
        fractal.root.after(10, fractal.createImage())
        fractal.run()

import profile
profile.run('start()')

