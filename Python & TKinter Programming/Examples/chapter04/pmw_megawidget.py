from Tkinter import *
import Pmw

class Gauge(Pmw.MegaWidget):
    def __init__(self, parent=None, **kw):

        # Define the options for the megawidget
        optiondefs = (
            ('min',           0,          Pmw.INITOPT),
            ('max',           100,        Pmw.INITOPT),
            ('fill',          'red',      None),
            ('size',          30,         Pmw.INITOPT),
            ('value',         0,          None),
            ('showvalue',     1,          None),
        )
        self.defineoptions(kw, optiondefs)

        # Initialize the base class
        Pmw.MegaWidget.__init__(self, parent)

        interior = self.interior()

        # Create the gauge component
        self.gauge = self.createcomponent('gauge',
                             (), None,
                             Frame, (interior,),
                             borderwidth=0)
        self.canvas = Canvas(self.gauge,
                             width=self['size'], height=self['size'],
                             background=interior.cget('background'))
        self.canvas.pack(side=TOP, expand=1, fill=BOTH, anchor=CENTER)
        self.gauge.grid()

        # Create the scale component
        self.scale = self.createcomponent('scale',
                             (), None,
                             Scale, (interior,),
                             command=self._setGauge,
                             length=200,
                             from_ = self['min'],
                             to    = self['max'],
                             showvalue=self['showvalue'])
        self.scale.grid()

        value=self['value']
        if value is not None:
            self.scale.set(value)

        # Check keywords and initialize options
        self.initialiseoptions(Gauge)

    def _setGauge(self, value):
        self.canvas.delete('gauge')
        ival = self.scale.get()
        ticks = self['max'] - self['min']
        arc = (360.0/ticks) * ival
        xy = 3,3,self['size'],self['size']
        start = 90-arc
        if start < 0:
            start = 360 + start
        self.canvas.create_arc(xy, start=start, extent=arc-.001,
                               fill=self['fill'], tags=('gauge',))

Pmw.forwardmethods(Gauge, Scale, 'scale')

root = Tk()
root.option_readfile('optionDB')
root.title('Gauge')
Pmw.initialise()

g1 = Gauge(root, fill='red', value=56, min=0, max=255)
g1.pack(side=LEFT, padx=1, pady=10)

g2 = Gauge(root, fill='green', value=60, min=0, max=255)
g2.pack(side=LEFT, padx=1, pady=10)

g3 = Gauge(root, fill='blue', value=36,  min=0, max=255)
g3.pack(side=LEFT, padx=1, pady=10)

root.mainloop()

