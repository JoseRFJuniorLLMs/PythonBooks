# SampleServer.py -- 
import string
import pythoncom
import pywintypes
import winerror
import types
from win32com.server.exception import COMException
from win32com.server.util import wrap
from win32com.server.policy import DynamicPolicy
from win32com.server.dispatcher import DefaultDebugDispatcher

simpleTypes = [
	types.StringType, pywintypes.UnicodeType,
	types.IntType, types.LongType, types.FloatType,
	types.TupleType, types.ListType,
]

def MakePythonObject(obj):
	# For simple types, we just return it
	objtype = type(obj)
	if objtype in simpleTypes:
		return obj
	else:
		print "Returning wrapped for", obj
		return wrap(PythonObject(obj), usePolicy=DynamicPolicy, useDispatcher = DefaultDebugDispatcher)

class PythonInterpreter:
    _reg_progid_ = "PythonDemos.Interpreter"
    _reg_clsid_ = "{5E7D60E2-D851-11D2-8530-204C4F4F5020}"
    _public_methods_ = ["Import", "Exec", "Eval"]

    def __init__(self):
        self.namespace = {}

    def _value_(self, name):
        try:
            return MakePythonObject(self.namespace[name])
        except KeyError:
            raise COMException("Unknown attribute", winerror.DISP_E_MEMBERNOTFOUND)

    def Exec(self, statement):
        exec statement in self.namespace
    
    def Eval(self, expression):
        return MakePythonObject(eval(expression, self.namespace))

    def Import(self, modName):
        try:
            mod = __import__(str(modName))
            self.namespace[modName] = mod
            return MakePythonObject(mod)
        except ImportError, msg:
            raise COMException(msg)

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

class PythonObject:
    # This is a Python object, but is not registered.
    # The only way to create a COM object of this type
    # is via the Interpreter objcet.
    def __init__(self, obj):
        self.obj = obj

    def _dynamic_(self, name, lcid, wFlags, args):
        if name=='_value_':
          return "Python object %s" % `self.obj`
        
        # Massage the arguments...
        args = FixArgs(args)
        if wFlags & pythoncom.DISPATCH_PROPERTYPUT:
            setattr(self.obj, name, args[0])
            return

        allattrs = dir(self.obj)
        try:
            allattrs = allattrs + dir(self.obj.__class__)
        except AttributeError:
            pass
        for attr in allattrs:
            if string.lower(attr)==name:
                item = getattr(self.obj, attr)
                break
        else:
            raise COMException("No attribute of that name", \
                               winerror.DISP_E_MEMBERNOTFOUND)

        print "Found", item, "as", `attr`
        if (wFlags & pythoncom.DISPATCH_METHOD) and \
           type(item) in [types.BuiltinFunctionType, types.FunctionType, types.ClassType]:
            return MakePythonObject(apply(item, args))
                          
        if wFlags & pythoncom.DISPATCH_PROPERTYGET:
            return MakePythonObject(item)
             
        raise COMException("Sorry - we dont support setting attributes", 
                           winerror.DISP_E_BADVARTYPE)

# Registration support.
if __name__=='__main__':
    import win32com.server.register
    win32com.server.register.UseCommandLine(PythonInterpreter)
