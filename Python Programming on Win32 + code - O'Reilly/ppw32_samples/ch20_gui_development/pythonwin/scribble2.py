# scribble2.py
#
# Most of the functionality for our scribble application.
import win32ui
import win32con
import pywin.mfc.docview
import pickle
import string
import os

class ScribbleTemplate(pywin.mfc.docview.DocTemplate):
    def MatchDocType(self, fileName, fileType):
        doc = self.FindOpenDocument(fileName)
        if doc: return doc
        ext = string.lower(os.path.splitext(fileName)[1])
        if ext =='.psd':
            return win32ui.CDocTemplate_Confidence_yesAttemptNative
        return win32ui.CDocTemplate_Confidence_noAttempt

class ScribbleDocument(pywin.mfc.docview.Document):
    def OnNewDocument(self):
        """Called whenever the document needs initializing.
        For most MDI applications, this is only called as the document
        is created.
        """
        self.strokes = []
        return 1
        
    def AddStroke(self, start, end, fromView):
        self.strokes.append((start, end))
        self.SetModifiedFlag()
        self.UpdateAllViews( fromView, None )
        
    def GetStrokes(self):
        return self.strokes

    def OnOpenDocument(self, filename):
        file = open(filename, "rb")
        self.strokes = pickle.load(file)
        file.close()
        win32ui.AddToRecentFileList(filename)
        return 1
        
    def OnSaveDocument(self, filename):
        file = open(filename, "wb")
        pickle.dump(self.strokes, file)
        file.close()
        self.SetModifiedFlag(0)
        win32ui.AddToRecentFileList(filename)
        return 1
    

class ScribbleView(pywin.mfc.docview.ScrollView):
    def OnInitialUpdate(self):
        self.SetScrollSizes(win32con.MM_TEXT, (0, 0))
        self.HookMessage(self.OnLButtonDown,win32con.WM_LBUTTONDOWN)
        self.HookMessage(self.OnLButtonUp,win32con.WM_LBUTTONUP)
        self.HookMessage(self.OnMouseMove,win32con.WM_MOUSEMOVE)
        self.bDrawing = 0
        
    def OnLButtonDown(self, params):
        assert not self.bDrawing, "Button down message while still drawing"
        startPos = params[5]
        # Convert the startpos to Client coordinates.
        self.startPos = self.ScreenToClient(startPos)
        self.lastPos = self.startPos
        # Capture all future mouse movement.
        self.SetCapture()
        self.bDrawing = 1
        
    def OnLButtonUp(self, params):
        assert self.bDrawing, "Button up message, but not drawing!"
        endPos = params[5]
        endPos = self.ScreenToClient(endPos)
        self.ReleaseCapture()
        self.bDrawing = 0
        # And add the stroke to the document.
        self.GetDocument().AddStroke( self.startPos, endPos, self )
        
    def OnMouseMove(self, params):
        # If Im not drawing at the moment, I don't care
        if not self.bDrawing:
            return
        pos = params[5]
        dc = self.GetDC()
        # Setup for an inverting draw operation.
        dc.SetROP2(win32con.R2_NOT)
    
        # "undraw" the old line
        dc.MoveTo(self.startPos)
        dc.LineTo(self.lastPos)

        # Now draw the new position
        self.lastPos = self.ScreenToClient(pos)
        dc.MoveTo(self.startPos)
        dc.LineTo(self.lastPos)
        
    def OnDraw(self, dc):
        # All we need to is get the strokes, and paint them.
        doc = self.GetDocument()
        for startPos, endPos in doc.GetStrokes():
            dc.MoveTo(startPos)
            dc.LineTo(endPos)


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

