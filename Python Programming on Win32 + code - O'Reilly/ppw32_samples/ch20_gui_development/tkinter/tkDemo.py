#!/usr/bin/env python
import sys, re, string
from Tkinter import *
from ScrolledText import ScrolledText

class Demo(Frame):
	def __init__(self, master):
		Frame.__init__(self, master, relief=RAISED, bd=2)
		l = Label(self, text=self.label, font=('Helvetica', 12, 'italic bold'),
				  background='dark slate blue', foreground='white')
		l.pack(side=TOP, expand=NO, fill=X)

class ReliefDemo(Demo):
	label = 'Relief types: Label widgets with 2d/3d borders'
	def __init__(self, master):
		Demo.__init__(self, master)
		for relief in [RAISED, SUNKEN, RIDGE, GROOVE, FLAT, SOLID]:
			l = Label(self, text=relief, relief=relief, bd=4)
			l.pack(side=LEFT, expand=YES, fill=BOTH,
				   padx=4, pady=4, ipadx=4, ipady=4)

class OptionDemo(Demo):
	label = 'OptionMenu:'
	def __init__(self, master):
		Demo.__init__(self, master)

		f = Frame(self)
		Label(f, text='Justify').pack(side=LEFT)
		op = OptionMenu(f, app.justifyVar, 'left', 'center', 'right')
		op.pack()
		f.pack()

		f = Frame(self)
		Label(f, text='Fit to').pack(side=LEFT)
		op = OptionMenu(f, app.sizeVar, 'minimum', 'maximum')
		op.pack()
		f.pack()

class CanvasDemo(Demo):
	label = 'Canvas widget with simple animation:'
	def __init__(self, master):
		Demo.__init__(self, master)
		self.canvas = Canvas(self, relief=SUNKEN, bd=2, background='gray65',
							 width=100, height=100)
		self.canvas.pack(side=TOP, expand=YES, fill=BOTH)
		self.arc = self.canvas.create_arc(0,0, 1,1)

		self.start, self.extent = 90,0

	def configure(self, event=None):
		fillColor = ''
		if app.fillVar.get(): fillColor = app.colorVar.get()

		outlineColor = ''
		if app.outlineVar.get(): outlineColor = 'black'
		
		self.canvas.itemconfigure(self.arc, style=app.styleVar.get())
		self.canvas.itemconfigure(self.arc, fill=fillColor)
		self.canvas.itemconfigure(self.arc, outline=outlineColor)
		
	def animate(self):
		w,h = self.canvas.winfo_width(), self.canvas.winfo_height()

		if app.sizeVar.get() == 'minimum':
			s = min(w,h)
		else:
			s = max(w,h)

		if app.justifyVar.get() == 'left':
			x0,x1 = 10, s-10
		elif app.justifyVar.get() == 'center':
			x0,x1 = (w-s+20)/2, (w+s-20)/2
		else:
			x0,x1 = w-s+10, w-10

		y0, y1 = (h-s+20)/2, (h+s-20)/2

		self.canvas.coords(self.arc, x0,y0, x1,y1)
		self.start  = self.start  - app.animateSpeed1.get()
		self.extent = self.extent - app.animateSpeed2.get()
		self.canvas.itemconfigure(self.arc,start=self.start,extent=self.extent)
		root.after(10, self.animate)

# A small collection (about 16%) of the colors found in the usual X11 color
# data base:  .../lib/X11/rgb.txt

COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white',
		  'old lace', 'linen', 'antique white', 'papaya whip',
		  'blanched almond', 'bisque', 'peach puff', 'navajo white',
		  'moccasin', 'cornsilk', 'ivory', 'lemon chiffon', 'seashell',
		  'honeydew', 'mint cream', 'azure', 'alice blue', 'lavender',
		  'lavender blush', 'misty rose', 'white', 'black', 'dark slate gray',
		  'dark slate grey', 'dim gray', 'dim grey', 'slate gray',
		  'slate grey', 'light slate gray', 'light slate grey', 'gray',
		  'grey', 'light grey', 'light gray', 'midnight blue', 'navy',
		  'navy blue', 'cornflower blue', 'dark slate blue', 'slate blue',
		  'medium slate blue', 'light slate blue', 'medium blue',
		  'royal blue', 'blue', 'dodger blue', 'deep sky blue', 'sky blue',
		  'light sky blue', 'steel blue', 'light steel blue', 'light blue',
		  'powder blue', 'pale turquoise', 'dark turquoise',
		  'medium turquoise', 'turquoise', 'cyan', 'light cyan', 'cadet blue',
		  'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
		  'dark sea green', 'sea green', 'medium sea green',
		  'light sea green', 'pale green', 'spring green', 'lawn green',
		  'green', 'chartreuse', 'medium spring green', 'green yellow',
		  'lime green', 'yellow green', 'forest green', 'olive drab',
		  'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
		  'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod',
		  'dark goldenrod', 'rosy brown', 'indian red', 'saddle brown',
		  'sienna', 'peru', 'burlywood', 'beige', 'wheat', 'sandy brown',
		  'tan', 'chocolate', 'firebrick', 'brown', 'dark salmon', 'salmon',
		  'light salmon', 'orange', 'dark orange', 'coral', 'light coral',
		  'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink',
		  'light pink', 'pale violet red', 'maroon', 'medium violet red',
		  'violet red', 'magenta', 'violet', 'plum', 'orchid',
		  'medium orchid', 'dark orchid', 'dark violet', 'blue violet',
		  'purple', 'medium purple', 'thistle', 'dark grey', 'dark gray',
		  'dark blue', 'dark cyan', 'dark magenta', 'dark red', 'light green']

COLORS.sort(lambda a,b: cmp(string.split(a)[-1], string.split(b)[-1]))

class ListboxDemo(Demo):
	label = 'Listbox, Entry, Button,\nand Scrollbar widgets:'
	def __init__(self, master):
		Demo.__init__(self, master)

		e = Entry(self, textvariable=app.colorVar)
		e.pack(side=TOP, fill=X)
		e.bind('<Return>', self.enterColor)
		
		b = Button(self, text='Select color', command=self.selectColor)
		b.pack(side=BOTTOM, fill=X)
		
		self.colorList = Listbox(self, height=6)
		self.colorList.pack(side=LEFT, expand=YES, fill=BOTH)
		for color in COLORS:
			self.colorList.insert(AtEnd(), color)
		self.colorList.selection_set(COLORS.index(app.colorVar.get()))

		scrollbar = Scrollbar(self)
		self.colorList.configure(yscrollcommand=(scrollbar, 'set'))
		scrollbar.configure(command=(self.colorList, 'yview'))
		scrollbar.pack(side=LEFT, fill=Y)

		self.colorList.bind("<Double-Button-1>", self.selectColor)

	def enterColor(self, event=None):
		app.canvasDemo.configure()

	def selectColor(self, event=None):
		colorIndex = map(string.atoi, app.listDemo.colorList.curselection())
		if not colorIndex: return
		app.colorVar.set(app.listDemo.colorList.get(colorIndex[0]))
		app.canvasDemo.configure()

def Char(c): return '0.0+%d char' % c
def Options(**kw): return kw

class TextDemo(Demo):
	label = 'Text widget displaying source with cheap syntax highlighting:\n'+\
			'(Move mouse over text and watch indent-structure highlighting.)'
	font = ('Courier', 10, 'normal')
	bold = ('Courier', 10, 'bold')
	Highlights = {'#.*': Options(foreground='red'),
				  r'\'.*?\'': Options(foreground='yellow'),
				  r'\bdef\b\s.*:':Options(foreground='blue', spacing1=2),
				  r'\bclass\b\s.*\n':Options(background='pink', spacing1=5),
				  r'\b(class|def|for|in|import|from|break|continue)\b':
				   Options(font=bold)
				  }
	
	def __init__(self, master):
		Demo.__init__(self, master)
		self.text = ScrolledText(self, width=80, height=20,
								 font=self.font, background='gray65',
								 spacing1=1, spacing2=1, tabs='24')
		self.text.pack(side=TOP, expand=YES, fill=BOTH)

		content = open(sys.argv[0], 'r').read()
		self.text.insert(AtEnd(), content)

		reg = re.compile('([\t ]*).*\n')
		pos = 0
		indentTags = []
		while 1:
			match = reg.search(content, pos)
			if not match: break
			indent = match.end(1)-match.start(1)
			if match.end(0)-match.start(0) == 1:
				indent = len(indentTags)
			tagb = 'Tagb%08d' % match.start(0)
			tagc = 'Tage%08d' % match.start(0)
			self.text.tag_configure(tagc, background='', relief=FLAT, borderwidth=2)
			self.text.tag_add(tagb, Char( match.start(0)), Char(match.end(0)))
			self.text.tag_bind(tagb, '<Enter>',
							   lambda e,self=self,tagc=tagc: self.Enter(tagc))
			self.text.tag_bind(tagb, '<Leave>',
							   lambda e,self=self,tagc=tagc: self.Leave(tagc))
			del indentTags[indent:]
			indentTags.extend( (indent-len(indentTags))*[None] )
			indentTags.append(tagc)
			for tag in indentTags:
				if tag:
					self.text.tag_add(tag, Char(match.start(0)),
									  Char(match.end(0)))
			pos = match.end(0)

		for key,kw in self.Highlights.items():
			self.text.tag_configure(key, cnf=kw)
			reg = re.compile(key)
			pos = 0
			while 1:
				match = reg.search(content, pos)
				if not match: break
				self.text.tag_add(key, Char(match.start(0)),Char(match.end(0)))
				pos = match.end(0)

	def Enter(self, tag):
		self.text.tag_raise(tag)
		self.text.tag_configure(tag, background='gray80', relief=RAISED)

	def Leave(self, tag):
		self.text.tag_configure(tag, background='', relief=FLAT)

MessageText = '''All the controls in this block control some aspect of the animation in the Canvas widget.  Most should be self explanitory.  To choose the fill color, do one of (a) type a color name into the Entry widget and RETURN, (b) select a color in the Listbox and hit "Select color" Button, or (c) double-click a color in the Listbox.'''

class MessageDemo(Demo):
	label = 'Message widget:'
	def __init__(self, master):
		Demo.__init__(self, master)
		self.message =  Message(self, text=MessageText)
		self.message.pack(side=TOP, expand=YES, fill=BOTH)
		self.message.bind('<Configure>', self.redoAspectRatio)
	def redoAspectRatio(self, event=None):
		w,h = self.message.winfo_width(), self.message.winfo_height()
		self.message.configure(aspect=(100*w)/h)

class RadiobuttonDemo(Demo):
	label = 'Radiobutton:'
	def __init__(self, master):
		Demo.__init__(self, master)
		self.count = IntVar()
		self.count.set(1)
		Radiobutton(self, text='Pie Slice',
					variable=app.styleVar, value='pieslice',
					command=app.canvasDemo.configure).pack(anchor=W)
		Radiobutton(self, text='Chord',
					variable=app.styleVar, value='chord',
					command=app.canvasDemo.configure).pack(anchor=W)
		Radiobutton(self, text='Arc only',
					variable=app.styleVar, value='arc',
					command=app.canvasDemo.configure).pack(anchor=W)
	
class CheckbuttonDemo(Demo):
	label = 'Checkbutton:'
	def __init__(self, master):
		Demo.__init__(self, master)
		Checkbutton(self, text='Fill', variable=app.fillVar,
					command=app.canvasDemo.configure).pack(anchor=W)
		Checkbutton(self, text='Outline', variable=app.outlineVar,
					command=app.canvasDemo.configure).pack(anchor=W)

class ScaleDemo(Demo):
	label = 'Scale:\n(animation speed)'
	def __init__(self, master):
		Demo.__init__(self, master)
		s1 = Scale(self, from_=-6.0, to=6.0,
				   resolution=0.1,
				   label='Start angle increment:',
				   orient=HORIZONTAL,
				   variable=app.animateSpeed1)
		s1.pack(side=TOP, expand=YES, fill=X)
		s2 = Scale(self, from_=-6.0, to=6.0,
				   resolution=0.1,
				   label='Extent angle increment:',
				   orient=HORIZONTAL,
				   variable=app.animateSpeed2)
		s2.pack(side=TOP, expand=YES, fill=X)

class MenubarDemo:

	def __init__(self, master):
		# Create the menu widgets, and register with their parents.
		menubar = Menu(root)
		master.config(menu=menubar)
	
		controlmenu = Menu(menubar)
		menubar.add_cascade(label='Controls', menu=controlmenu)
		
		radiomenu = Menu(menubar)
		controlmenu.add_cascade(label='Radiobutton menu', menu=radiomenu)
	
		checkmenu = Menu(menubar)
		controlmenu.add_cascade(label='Checkbutton menu', menu=checkmenu)
	
		# Add the command(s) to the menu(s)
		controlmenu.add_command(label='Exit', foreground='red',
								command=sys.exit)

		radiomenu.add_radiobutton(label='Pie Slice', command=self.notify,
								  variable=app.styleVar, value='pieslice')
		radiomenu.add_radiobutton(label='Chord', command=self.notify,
								  variable=app.styleVar, value='chord')
		radiomenu.add_radiobutton(label='Arc only', command=self.notify,
								  variable=app.styleVar, value='arc')

		checkmenu.add_checkbutton(label='Fill', command=self.notify,
								  variable=app.fillVar, onvalue=1, offvalue=0)
		checkmenu.add_checkbutton(label='Outline', command=self.notify,
								  variable=app.outlineVar,onvalue=1,offvalue=0)
			
							  
	def notify(self):
		app.canvasDemo.configure()

						   
	

class Application:
	def __init__(self):
		root.title('tkDemo: Demonstration of Tk widgets')
		self.styleVar = StringVar();		self.styleVar.set('pieslice')
		self.fillVar = BooleanVar();		self.fillVar.set(1)
		self.outlineVar = BooleanVar();		self.outlineVar.set(1)
		self.animateSpeed1 = DoubleVar();	self.animateSpeed1.set(1.0)
		self.animateSpeed2 = DoubleVar();	self.animateSpeed2.set(1.0)
		self.colorVar = StringVar();		self.colorVar.set('aquamarine')
		self.justifyVar = StringVar();		self.justifyVar.set('center')
		self.sizeVar = StringVar();			self.sizeVar.set('minimum')
		
	def Go(self):
		MenubarDemo(root)
		self.reliefDemo = ReliefDemo(root)
		self.messageDemo = MessageDemo(root)
		self.canvasDemo = CanvasDemo(root)
		self.optionDemo = OptionDemo(root)
		self.listDemo = ListboxDemo(root)
		self.radioDemo = RadiobuttonDemo(root)
		self.checkDemo = CheckbuttonDemo(root)
		self.scaleDemo = ScaleDemo(root)
		self.textDemo = TextDemo(root)

		self.PackAll(
		[
			[[self.reliefDemo]],
			[[self.messageDemo,self.listDemo,self.scaleDemo],
			 [self.canvasDemo,self.radioDemo,self.checkDemo,self.optionDemo]],
			[[self.textDemo]]
		])

		self.canvasDemo.configure()
		self.canvasDemo.animate()
		
		root.mainloop()

	def PackAll(self, batches):
		for batch in batches:
			b = Frame(root, bd=15, relief=FLAT)
			for row in batch:
				f = Frame(b)
				for widget in row:
					widget.pack(in_=f, side=LEFT, expand=YES, fill=BOTH)
					widget.tkraise()
				f.pack(side=TOP, expand=YES, fill=BOTH)
			b.pack(side=TOP, expand=YES, fill=BOTH)

root = Tk()

if __name__ == '__main__':
	app = Application()
	app.Go()
