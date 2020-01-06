# ActiveApp.py - Demonstration of a Python Active Scripting Application.
import string, sys
from win32com.axscript import axscript
from win32com.axscript.server import axsite
import pythoncom
import win32com.server.util

class MySite(axsite.AXSite):
    # Our error handler will simply print to the console.
    def OnScriptError(self, activeScriptError):
        exc = activeScriptError.GetExceptionInfo()
        print "Exception:", exc[1]
        try:
            sourceText = activeScriptError.GetSourceLineText()
        except pythoncom.com_error:
            sourceText = None
        if sourceText is not None: 
            context, lineNo, charNo = activeScriptError.GetSourcePosition()
            print sourceText
            indent = " " * (charNo-1)
            print indent + "^"
        return winerror.S_OK

# A named object for our namespace
# A normal Python COM object (minus registration info)
class Application:
    _public_methods_ = [ 'Echo' ]
    def Echo(self, *args):
        print string.join(map(str, args))

# Our function that creates the site, creates the engine
# and runs the code.
def RunCode(engineName, code):
    app = win32com.server.util.wrap( Application() )
    # Create a dictionary holding our object model.
    model = {
      'Application' : app,
    }

    # Create the scripting site.
    site = MySite(model)
    # Create the engine and add the code.
    engine = site.AddEngine(engineName)
    engine.AddCode(code)
    # Run the code.
    engine.Start()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: ActiveApp.py Language ScriptFile"
    else:
        code = open(sys.argv[2]).read()
        RunCode( sys.argv[1], code )

