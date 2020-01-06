# ThreadingModelsServer.py
# Python COM objects that demonstrate COM threading models.
#
# Exposes 3 Python objects, all of which have identical functionality,
# but each indicate they support different threading models.

import win32api
# A Base class for our 2 trivial objects.
class ThreadDemoObject:
    _public_methods_ = [ 'GetCurrentThreadId', 'GetCreatedThreadId' ]
    def __init__(self):
        self.created_id = win32api.GetCurrentThreadId()
    def GetCreatedThreadId(self):
        return self.created_id
    def GetCurrentThreadId(self):
        # Simply return an integer with the Win32 thread ID.
        return win32api.GetCurrentThreadId()

class ThreadApartmentObject(ThreadDemoObject):
    _reg_threading_ = "Apartment" # Tell COM to synchronize
    _reg_progid_ = "PythonThreadDemo.Apartment"
    _reg_clsid_ = "{511BB541-4625-11D3-855B-204C4F4F5020}"

class ThreadFreeObject(ThreadDemoObject):
    _reg_threading_ = "Free"
    _reg_progid_ = "PythonThreadDemo.Free"
    _reg_clsid_ = "{511BB542-4625-11D3-855B-204C4F4F5020}"

class ThreadBothObject(ThreadDemoObject):
    _reg_threading_ = "Both"
    _reg_progid_ = "PythonThreadDemo.Both"
    _reg_clsid_ = "{511BB543-4625-11D3-855B-204C4F4F5020}"

if __name__=='__main__':
    import win32com.server.register
    win32com.server.register.UseCommandLine(
                       ThreadApartmentObject,
                       ThreadFreeObject,
                       ThreadBothObject)
