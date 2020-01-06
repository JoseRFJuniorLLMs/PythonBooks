# scribble1.py
#
# The starting framework for our scribble application.
import win32ui
import win32con
import pywin.mfc.docview

class ScribbleTemplate(pywin.mfc.docview.DocTemplate):
    pass

class ScribbleDocument(pywin.mfc.docview.Document):
    def OnNewDocument(self):
        """Called whenever the document needs initializing.
        For most MDI applications, this is only called as the document
        is created.
        """
        self.strokes = []
        return 1

class ScribbleView(pywin.mfc.docview.ScrollView):
    def OnInitialUpdate(self):
        self.SetScrollSizes(win32con.MM_TEXT, (0, 0))

# Now we do the work to create the document template, and
# register it with the framework.

# For debugging purposes, we first attempt to remove the old template.
# This is not necessary once our app becomes stable!
try:
    win32ui.GetApp().RemoveDocTemplate(template)
except NameError:
    # havent run this before - thats ok
    pass

# Now create the template object itself...
template = ScribbleTemplate(None, ScribbleDocument, None, ScribbleView)
# Set the doc strings for the template.
docs='\nPyScribble\nPython Scribble Document\nScribble documents (*.psd)\n.psd'
template.SetDocStrings(docs)

# Then register it with MFC.
win32ui.GetApp().AddDocTemplate(template)
