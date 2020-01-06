# scribbleApp.py
#
# The application object for Python.
from pywin.framework.app import CApp

class ScribbleApplication(CApp):
	def InitInstance(self):
		# All we need do is call the base class,
		# then import our document template.
		CApp.InitInstance(self)
		import scribble2
		
# And create our application object.
ScribbleApplication()