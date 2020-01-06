# SimpleCOMServer.py - A sample COM server - almost as small as they come!
# 
# We simply expose a single method in a Python COM object.
class PythonUtilities:
    _public_methods_ = [ 'SplitString' ]
    _reg_progid_ = "PythonDemos.Utilities"
    # NEVER copy the following ID 
    # Use "print pythoncom.CreateGuid()" to make a new one.
    _reg_clsid_ = "{41E24E95-D45A-11D2-852C-204C4F4F5020}"
    
    def SplitString(self, val, item=None):
        import string
        if item != None: item = str(item)
        return string.split(str(val), item)

# Add code so that when this script is run by
# Python.exe, it self-registers.
if __name__=='__main__':
    print "Registering COM server..."
    import win32com.server.register
    win32com.server.register.UseCommandLine(PythonUtilities)
