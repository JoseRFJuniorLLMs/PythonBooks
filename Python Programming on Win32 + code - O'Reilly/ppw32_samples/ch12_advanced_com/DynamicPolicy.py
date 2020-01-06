# DynamicPolicy.py -- A demonstration of dynamic policies in PythonCOM
import string
import pythoncom
import pywintypes
import winerror
import types
from win32com.server.exception import COMException

def FixArgs(args):
    # Fix the arguments, so Unicode objects are
    # converted to strings.  Does this recursively,
    # to ensure sub-lists (ie, arrays) are also converted
    newArgs = []
    for arg in args:
        if type(arg)==types.TupleType:
            arg = FixArgs(arg)
        elif type(arg)==pywintypes.UnicodeType:
            arg = str(arg)
        newArgs.append(arg)
    return tuple(newArgs)

class PythonStringModule:
    _reg_progid_ = "PythonDemos.StringModule"
    _reg_clsid_ = "{CB2E1BC5-D6A5-11D2-852D-204C4F4F5020}"
    _reg_policy_spec_ = "DynamicPolicy"

    # The dynamic policy insists that we provide a method
    # named _dynamic_, and that we handle the IDispatch::Invoke logic.
    def _dynamic_(self, name, lcid, wFlags, args):
        # Get the requested attribute from the string module.
        try:
            item = getattr(string, string.lower(name))
        except AttributeError:
            raise COMException("No attribute of that name", \
                               winerror.DISP_E_MEMBERNOTFOUND)
        # Massage the arguments...
        args = FixArgs(args)
        # VB will often make calls with wFlags set to
        # DISPATCH_METHOD | DISPATCH_PROPERTYGET, as the VB
        # syntax makes the distinction impossible to make.
        # Therefore, we also check the object being referenced is
        # in fact a Python function
        if (wFlags & pythoncom.DISPATCH_METHOD) and \
           type(item) in [types.BuiltinFunctionType, types.FunctionType]:
            return apply(item, args)
        elif wFlags & pythoncom.DISPATCH_PROPERTYGET:
            return item
        else:
            raise COMException("You can not set this attribute", 
                               winerror.DISP_E_BADVARTYPE)

# Add code so that when this script is run by
# Python.exe, it self-registers.
if __name__=='__main__':
    import win32com.server.register
    win32com.server.register.UseCommandLine(PythonStringModule)
