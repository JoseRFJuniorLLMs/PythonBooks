# stuff for viewing 
# also does very basic 3d graphics



import win32ui
import win32con
import win32api
import docview
import string
import packobjects
import basic3d

def RGB(red, green, blue):
	return red + (256 * green) + (65536 * blue)

CARDCOLOUR = RGB(192,192,0)
CARDBRUSH = win32ui.CreateBrush(0, CARDCOLOUR,0)

class Controller:
	"holds the bookset, notifies the views of changes"
	def __init__(self):
		#self.BookSet = fastran.BookSet()
		self.views = []

		
	def loadData(self):
		#self.BookSet.loadDbl(DATADIR + '\\' + DATAFILE)
		pass
		
	def makeView(self, viewClass):
		#adds a new one
		#this is hideous - I am circumventing the whole of MFC just
		#'cos I don;t know how it works.
		template = docview.DocTemplate(win32ui.IDR_PYTHONTYPE, None, None, viewClass)
		doc=template.OpenDocumentFile(None)
		doc.SetTitle (repr(viewClass))
		template.close()
		del template
		view = doc.GetFirstView()
		view.controller = self
		self.views.append(view)
		#view.DataHasChanged(None)
		return view

	def redrawAll(self):
		for v in self.views:
			v.DataHasChanged(None)	
			 
class DtBaseView(docview.ScrollView):
	"Just playing around.  This should display a list of lists of strings"
	def __init__(self,  doc, text = 'Doubletalk Rules!'):
		docview.ScrollView.__init__(self, doc)
		self.table = map(str,range(10))
		self.width = self.height = 0
		#self.font = win32ui.CreateFont ({'name':'Arial', 'height':12})
		self.HookMessage (self.OnSize, win32con.WM_SIZE)		

	#def OnAttachedObjectDeath(self):
	#	docview.ScrollView.OnAttachedObjectDeath(self)
	#	del self.font

	def DataHasChanged (self, changeDesc):
		#base view does nothing
		self.InvalidateRect()

	def OnSize (self, params):
		lParam = params[3]
		self.width = win32api.LOWORD(lParam)
		self.height = win32api.HIWORD(lParam)

	def OnPrepareDC (self, dc, printinfo):
		self.SetScrollSizes(win32con.MM_TEXT, (100,100))

	def OnDraw (self, dc):
		#by default, draws line-by-line data
		x = y = 10
		for row in self.table:
			dc.TextOut (x, y, row)			
			y = y + 15
		dc.LineTo(100,100)		
			
class LineDrawingView(DtBaseView):
	def OnDraw (self, dc):
		#by default, draws line-by-line data
		x = y = 10
		dc.TextOut (x, y, 'a square')
		dc.MoveTo(50,50)			
		dc.LineTo(50,100)
		dc.LineTo(100,100)
		dc.LineTo(100,50)
		dc.LineTo(50,50)
		
		# make a brush
		#polygon
		dc.Polygon([(150,20),(175,80),(190,30)])
		dc.SelectObject(oldbrush)
		
		
		# Fill Solid Rect
		dc.FillSolidRect((200,21,299,79),CARDCOLOUR)
		
		
				
def view2d(aPack):
	C = Controller()
	v = C.makeView(PackView)
	v.Pack = aPack
	C.redrawAll()
	return v


def demo():
	C = Controller()
	v = C.makeView(LineDrawingView)
	print 'about to redraw'
	C.redrawAll()