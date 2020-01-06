from Tkinter import *
from Canvas import Line, CanvasText, Rectangle
import string, math
from utils import *
from math import pi
import Pmw

class GraphPoints:
    def __init__(self, points, attr):
        self.points = points
	self.scaled = self.points
        self.attributes = {}
        for name, value in self._attributes.items():
            try:
                value = attr[name]
            except KeyError: pass
            self.attributes[name] = value

    def boundingBox(self):
        return minBound(self.points),  maxBound(self.points)

    def fitToScale(self, scale=(1,1), shift=(0,0)):
        self.scaled = []
        for x,y in self.points:
            self.scaled.append((scale[0]*x)+shift[0],
                               (scale[1]*y)+shift[1])
            self.attributes.get('anchor', 0.0)
        self.anchor = scale[1]*self.attributes.get('anchor', 0.0)\
                      + shift[1]

class GraphLine(GraphPoints):
    def __init__(self, points, **attr):
        GraphPoints.__init__(self, points, attr)

    _attributes = {'color':       'black',
                   'width':        1,
                   'smooth':       0,
                   'splinesteps': 12}

    def draw(self, canvas, multi):
	color  = self.attributes['color']
	width  = self.attributes['width']
        smooth = self.attributes['smooth']
        steps  = self.attributes['splinesteps']
	arguments = (canvas,)
        if smooth:
            for i in range(len(self.points)):
                x1, y1 = self.scaled[i]
                arguments = arguments + (x1, y1)
        else:
            for i in range(len(self.points)-1):
                x1, y1 = self.scaled[i]
                x2, y2 = self.scaled[i+1]
                arguments = arguments + (x1, y1, x2, y2)
	apply(Line, arguments, {'fill': color, 'width': width,
                                'smooth': smooth,
                                'splinesteps': steps})

class GraphSymbols(GraphPoints):
    def __init__(self, points, **attr):
        GraphPoints.__init__(self, points, attr)

    _attributes = {'color': 'black',
                   'width': 1,
                   'fillcolor': 'black',
                   'size': 2,
                   'fillstyle': '',
                   'outline': 'black',
                   'marker': 'circle'}

    def draw(self, canvas, multi):
	color     = self.attributes['color']
        size      = self.attributes['size']
        fillcolor = self.attributes['fillcolor']
        marker    = self.attributes['marker']
        fillstyle = self.attributes['fillstyle']

	self._drawmarkers(canvas, self.scaled, marker, color,
                          fillstyle, fillcolor, size)

    def _drawmarkers(self, c, coords, marker='circle', color='black',
                     fillstyle='', fillcolor='', size=2):
        l = []
        f = eval('self._' +marker)
        for xc, yc in coords:
            id = f(c, xc, yc, outline=color, size=size,
                   fill=fillcolor, fillstyle=fillstyle)
            if type(id) is type(()):
                for item in id: l.append(item)
            else:
                l.append(id)
        return l
    
    def _circle(self, c, xc, yc, size=1, fill='', outline='black',
                fillstyle=''):
        id = c.create_oval(xc-0.5, yc-0.5, xc+0.5, yc+0.5, 
                           fill=fill, outline=outline,
                           stipple=fillstyle)
        c.scale(id, xc, yc, size*5, size*5)
        return id

    def _dot(self, c, xc, yc, size=1, fill='', outline='black',
             fillstyle=''):
        id = c.create_oval(xc-0.5, yc-0.5, xc+0.5, yc+0.5, 
                           fill=fill, outline=outline,
                           stipple=fillstyle)
        c.scale(id, xc, yc, size*2.5, size*2.5)
        return id

    def _square(self, c, xc, yc, size=1, fill='', outline='black',
                fillstyle=''):
        id = c.create_rectangle(xc-0.5, yc-0.5, xc+0.5, yc+0.5,
                                fill=fill, outline=outline,
                                stipple=fillstyle)
        c.scale(id, xc, yc, size*5, size*5)
        return id
    
    def _triangle(self, c, xc, yc, size=1, fill='', outline='black',
                  fillstyle=''):
        id = c.create_polygon(-0.5, 0.288675134595,
                              0.5, 0.288675134595,
                              0.0, -0.577350269189, fill=fill,
                              outline=outline, stipple=fillstyle)
        c.move(id, xc, yc)
        c.scale(id, xc, yc, size*5, size*5)
        return id

    def _triangle_down(self, c, xc, yc, size=1, fill='',
                       outline='black', fillstyle=''):
        id = c.create_polygon(-0.5, -0.288675134595,
                              0.5, -0.288675134595,
                              0.0, 0.577350269189, fill=fill,
                              outline=outline, stipple=fillstyle)
        c.move(id, xc, yc)
        c.scale(id, xc, yc, size*5, size*5)
        return id

    def _cross(self, c, xc, yc, size=1, fill='black', outline=None,
               fillstyle=''):
        if outline: fill=outline
        id1 = c.create_line(xc-0.5, yc-0.5, xc+0.5, yc+0.5,
                            fill=fill)
        id2 = c.create_line(xc-0.5, yc+0.5, xc+0.5, yc-0.5,
                            fill=fill)
        c.scale(id1, xc, yc, size*5, size*5)
        c.scale(id2, xc, yc, size*5, size*5)
        return id1, id2

    def _plus(self, c, xc, yc, size=1, fill='black', outline=None,
              fillstyle=''):
        if outline: fill=outline
        id1 = c.create_line(xc-0.5, yc, xc+0.5, yc, fill=fill)
        id2 = c.create_line(xc, yc+0.5, xc, yc-0.5, fill=fill)
        c.scale(id1, xc, yc, size*5, size*5)
        c.scale(id2, xc, yc, size*5, size*5)
        return id1, id2

class GraphBars(GraphPoints):
    def __init__(self, points, **attr):
        GraphPoints.__init__(self, points, attr)

    _attributes = {'color': 'black',
                   'width': 1,
                   'fillcolor': 'yellow',
                   'size': 3,
                   'fillstyle': '', 
                   'outline': 'black'}

    def draw(self, canvas, multi):
	color     = self.attributes['color']
	width     = self.attributes['width']
        fillstyle = self.attributes['fillstyle']
        outline   = self.attributes['outline']
        spread    = self.attributes['size']
	arguments = (canvas,)
        p1, p2    = self.boundingBox()
        for i in range(len(self.points)):
            x1, y1 = self.scaled[i]
            canvas.create_rectangle(x1-spread, y1, x1+spread,
                                    self.anchor, fill=color,
                                    width=width, outline=outline,
                                    stipple=fillstyle)
    
class GraphPie(GraphPoints):
    def __init__(self, points, **attr):
        GraphPoints.__init__(self, points, attr)

    _attributes = {'color': 'black',
                   'width': 1,
                   'fillcolor': 'yellow',
                   'size': 2,
                   'fillstyle': '', 
                   'outline': 'black'}

    def draw(self, canvas, multi):
	width     = self.attributes['width']
        fillstyle = self.attributes['fillstyle']
        outline   = self.attributes['outline']
        colors    = Pmw.Color.spectrum(len(self.scaled))
	arguments = (canvas,)
        
        x1 = string.atoi(canvas.cget('width'))
        y1 = string.atoi(canvas.cget('height'))
        adj = 0
        if multi: adj = 15
        xy  = 25+adj, 25+adj, x1-25-adj, y1-25-adj
        xys = 25+adj, 25+adj+10, x1-25-adj, y1-25-adj+10
        tt = 0.0
        i = 0
        for point in self.points:
            tt = tt + point[1]
        start = 0.0
        if not x1 == y1:
            canvas.create_arc(xys, start=0.0, extent=359.99,
                              fill='gray60', outline=outline,
                              style='pieslice')
        for point in self.points:
            x1, y1 = point
            extent = (y1/tt)*360.0
            canvas.create_arc(xy, start=start, extent=extent,
                              fill=colors[i], width=width,
                              outline=outline, stipple=fillstyle,
                              style='pieslice')
            start = start + extent
            i = i+1
    
class GraphObjects:
    def __init__(self, objects):
        self.objects  = objects
        self.multiple = len(objects)-1
        
    def boundingBox(self):
	c1, c2 = self.objects[0].boundingBox()
	for object in self.objects[1:]:
	    c1o, c2o = object.boundingBox()
	    c1 = minBound([c1, c1o])

	    c2 = maxBound([c2, c2o])
	return c1, c2

    def fitToScale(self, scale=(1,1), shift=(0,0)):
	for object in self.objects:
	    object.fitToScale(scale, shift)

    def draw(self, canvas):
	for object in self.objects:
	    object.draw(canvas, self.multiple)

class GraphBase(Frame):
    def __init__(self, master, width, height,
                 background='white', **kw):
        apply(Frame.__init__, (self, master), kw)
	self.canvas = Canvas(self, width=width, height=height,
			     background=background)
	self.canvas.pack(fill=BOTH, expand=YES)
        border_w = self.canvas.winfo_reqwidth() - \
                   string.atoi(self.canvas.cget('width'))
        border_h = self.canvas.winfo_reqheight() - \
                   string.atoi(self.canvas.cget('height'))
        self.border = (border_w, border_h)
        self.canvas.bind('<Configure>', self.configure)
        self.plotarea_size = [None, None]
	self._setsize()
	self.last_drawn = None
	self.font = ('Verdana', 10)

    def configure(self, event):
        new_width = event.width-self.border[0]
        new_height = event.height-self.border[1]
        width = string.atoi(self.canvas.cget('width'))
        height = string.atoi(self.canvas.cget('height'))
        if new_width == width and new_height == height:
            return
        self.canvas.configure(width=new_width, height=new_height)
        self._setsize()
        self.clear()
        self.replot()

    def bind(self, *args):
        apply(self.canvas.bind, args)

    def _setsize(self):
	self.width = string.atoi(self.canvas.cget('width'))
	self.height = string.atoi(self.canvas.cget('height'))
	self.plotarea_size[0] = 0.97 * self.width
	self.plotarea_size[1] = 0.97 * -self.height      
	xo = 0.5*(self.width-self.plotarea_size[0])
	yo = self.height-0.5*(self.height+self.plotarea_size[1])
	self.plotarea_origin = (xo, yo)
        
    def draw(self, graphics, xaxis = None, yaxis = None):
	self.last_drawn = (graphics, xaxis, yaxis)
	p1, p2 = graphics.boundingBox()
	xaxis = self._axisInterval(xaxis, p1[0], p2[0])
	yaxis = self._axisInterval(yaxis, p1[1], p2[1])
	text_width = [0., 0.]
	text_height = [0., 0.]
	if xaxis is not None:
	    p1 = xaxis[0], p1[1]
	    p2 = xaxis[1], p2[1]
 	    xticks = self._ticks(xaxis[0], xaxis[1])
 	    bb = self._textBoundingBox(xticks[0][1])
 	    text_height[1] = bb[3]-bb[1]
 	    text_width[0] = 0.5*(bb[2]-bb[0])
 	    bb = self._textBoundingBox(xticks[-1][1])
 	    text_width[1] = 0.5*(bb[2]-bb[0])
	else:
	    xticks = None
	if yaxis is not None:
	    p1 = p1[0], yaxis[0]
	    p2 = p2[0], yaxis[1]
 	    yticks = self._ticks(yaxis[0], yaxis[1])
 	    for y in yticks:
		bb = self._textBoundingBox(y[1])
		w = bb[2]-bb[0]
		text_width[0] = max(text_width[0], w)
	    h = 0.5*(bb[3]-bb[1])
	    text_height[0] = h
	    text_height[1] = max(text_height[1], h)
	else:
	    yticks = None
	text1 = [text_width[0], -text_height[1]]
	text2 = [text_width[1], -text_height[0]]
 	scale = ((self.plotarea_size[0]-text1[0]-text2[0]) / \
                 (p2[0]-p1[0]),
                 (self.plotarea_size[1]-text1[1]-text2[1]) / \
                 (p2[1]-p1[1]))
 	shift = ((-p1[0]*scale[0]) + self.plotarea_origin[0] + \
                 text1[0],
                 (-p1[1]*scale[1]) + self.plotarea_origin[1] + \
                 text1[1])
	self._drawAxes(self.canvas, xaxis, yaxis, p1, p2,
                       scale, shift, xticks, yticks)
	graphics.fitToScale(scale, shift)
	graphics.draw(self.canvas)

    def _axisInterval(self, spec, lower, upper):
	if spec is None:
	    return None
	if spec == 'minimal':
	    if lower == upper:
		return lower-0.5, upper+0.5
	    else:
		return lower, upper
	if spec == 'automatic':
	    range = upper-lower
	    if range == 0.:
		return lower-0.5, upper+0.5
	    log = math.log10(range)
	    power = math.floor(log)
	    fraction = log-power
	    if fraction <= 0.05:
		power = power-1
	    grid = 10.**power
	    lower = lower - lower % grid
	    mod = upper % grid
	    if mod != 0:
		upper = upper - mod + grid
	    return lower, upper
	if type(spec) == type(()):
	    lower, upper = spec
	    if lower <= upper:
		return lower, upper
	    else:
		return upper, lower
	raise ValueError, str(spec) + ': illegal axis specification'

    def _drawAxes(self, canvas, xaxis, yaxis,
                  bb1, bb2, scale, shift, xticks, yticks):
	dict = {'anchor': N, 'fill': 'black'}
	if self.font is not None:
	    dict['font'] = self.font
	if xaxis is not None:
	    lower, upper = xaxis
	    text = 1
	    for y, d in [(bb1[1], -3), (bb2[1], 3)]:
		p1 = (scale[0]*lower)+shift[0], (scale[1]*y)+shift[1]
		p2 = (scale[0]*upper)+shift[0], (scale[1]*y)+shift[1]
		Line(self.canvas, p1[0], p1[1], p2[0], p2[1],
                     fill = 'black', width = 1)
                if xticks:
                    for x, label in xticks:
                        p = (scale[0]*x)+shift[0], \
                            (scale[1]*y)+shift[1]
                        Line(self.canvas, p[0], p[1], p[0], p[1]+d,
                             fill = 'black', width = 1)
                        if text:
                            dict['text'] = label
                            apply(CanvasText, (self.canvas, p[0],
                                               p[1]), dict)
		text = 0

	dict['anchor'] = E
	if yaxis is not None:
	    lower, upper = yaxis
	    text = 1
	    for x, d in [(bb1[0], -3), (bb2[0], 3)]:
		p1 = (scale[0]*x)+shift[0], (scale[1]*lower)+shift[1]
		p2 = (scale[0]*x)+shift[0], (scale[1]*upper)+shift[1]
		Line(self.canvas, p1[0], p1[1], p2[0], p2[1],
                     fill = 'black', width = 1)
                if yticks:
                    for y, label in yticks:
                        p = (scale[0]*x)+shift[0], \
                            (scale[1]*y)+shift[1]
                        Line(self.canvas, p[0], p[1], p[0]-d, p[1],
                             fill = 'black', width = 1)
                        if text:
                            dict['text'] = label
                            apply(CanvasText,(self.canvas,
                                              p[0]-2,p[1]), dict)
		text = 0

    def _ticks(self, lower, upper):
	ideal = (upper-lower)/7.
	log = math.log10(ideal)
	power = math.floor(log)
	fraction = log-power
	factor = 1.
	error = fraction
	for f, lf in self._multiples:
	    e = math.fabs(fraction-lf)
	    if e < error:
		error = e
		factor = f
	grid = factor * 10.**power
        if power > 3 or power < -3:
            format = '%+7.0e'
        elif power >= 0:
            digits = max(1, int(power))
            format = '%' + `digits`+'.0f'
        else:
            digits = -int(power)
            format = '%'+`digits+2`+'.'+`digits`+'f'
	ticks = []
	t = -grid*math.floor(-lower/grid)
	while t <= upper and len(ticks) < 200:
	    ticks.append(t, format % (t,))
	    t = t + grid
	return ticks

    _multiples = [(2., math.log10(2.)), (5., math.log10(5.))]

    def _textBoundingBox(self, text):
	bg = self.canvas.cget('background')
	dict = {'anchor': NW, 'text': text, 'fill': bg}
	if self.font is not None:
	    dict['font'] = self.font
	item = apply(CanvasText, (self.canvas, 0., 0.), dict)
	bb = self.canvas.bbox(item)
	self.canvas.delete(item)
	return bb

    def replot(self):
	if self.last_drawn is not None:
	    apply(self.draw, self.last_drawn)

    def clear(self):
        self.canvas.delete('all')

if __name__ == '__main__':

    root = Tk()
    root.title('Graph Widget - Piechart')

    pie1      = GraphPie([(0,21),(1,77),(2,129),(3,169),(4,260),(5,377),
                          (6,695),(7,434)])
    pie2      = GraphPie([(0,5),(1,22),(2,8),(3,45),(4,22),
                          (5,9),(6,40),(7,2),(8,56),(9,34),
                          (10,51),(11,43),(12,12),(13,65),(14,22),
                          (15,15),(16,48),(17,16),(18,45),(19,19),
                          (20,33)], fillstyle='gray50', width=2)
    pie3      = GraphPie([(0,5),(1,22),(2,8),(3,45),(4,22),
                          (5,9),(6,40),(7,2),(8,56),(9,34),
                          (10,51),(11,43),(12,12),(13,65),(14,22),
                          (15,15),(16,48),(17,16),(18,45),(19,19),
                          (20,33)])
    pieline4  = GraphLine([(0,21),(1,77),(2,129),(3,169),(4,260),
                           (5,377),(6,695),(7,434)], width=3)
    pielines4 = GraphSymbols([(0,21),(1,77),(2,129),(3,169),(4,260),
                              (5,377),(6,695),(7,434)],
                             marker='square', fillcolor='yellow')

    graphObject1 = GraphObjects([pie1])
    graphObject2 = GraphObjects([pie2])
    graphObject3 = GraphObjects([pie3])
    graphObject4 = GraphObjects([pie1, pieline4, pielines4])

    f1 = Frame(root)
    f2 = Frame(root)

    graph1  = GraphBase(f1, 300, 300, relief=SUNKEN, border=2)
    graph1.pack(side=LEFT, fill=BOTH, expand=YES)
    graph1.draw(graphObject1)

    graph2  = GraphBase(f1, 300, 300, relief=SUNKEN, border=2)
    graph2.pack(side=LEFT, fill=BOTH, expand=YES)
    graph2.draw(graphObject2)
     
    graph3  = GraphBase(f2, 300, 200, relief=SUNKEN, border=2)
    graph3.pack(side=LEFT, fill=X, expand=NO)
    graph3.draw(graphObject3)

    graph4  = GraphBase(f2, 300, 300, relief=SUNKEN, border=2)
    graph4.pack(side=LEFT, fill=BOTH, expand=YES)
    graph4.draw(graphObject4, 'automatic', 'automatic')

    f1.pack(side=TOP)
    f2.pack(side=TOP)

    frame3=Frame(root, bd=1, relief=SUNKEN)
    Button(frame3, text='Quit', command=root.quit).pack(side=RIGHT,
                                                        pady=3)
    frame3.pack(side=TOP, expand=YES, fill=BOTH)
    
    root.mainloop()
