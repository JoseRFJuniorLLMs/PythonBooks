# ContrivedServer.py
#
# A contrived sample Python server that demonstrates 
# wrapping, unwrapping, and passing IDispatch objects.

# Import the utilities for wrapping and unwrapping.
from win32com.server.util import wrap, unwrap

import win32com.client

# Although we are able to register our Parent object for debugging,
# our Child object is not registered, so this wont work. To get
# the debugging behavior for our wrapped objects, we must do it ourself.
debugging = 1
if debugging:
    from win32com.server.dispatcher import DefaultDebugDispatcher
    useDispatcher = DefaultDebugDispatcher
else:
    useDispatcher = None

# Our Parent object.
# This is registered, and therefore creatable
# using CreateObject etc from VB.
class Parent:
    _public_methods_ = ['CreateChild', 'KissChild']
    _reg_clsid_ = "{E8F7F001-DB69-11D2-8531-204C4F4F5020}"
    _reg_progid_ = "PythonDemos.Parent"

    def CreateChild(self):
        # We create a new Child object, and wrap
        # it up using the default policy
        # If we are debugging, we also specify the default dispatcher
        child = Child()
        print "Our Python child is", child
        wrapped = wrap( child, useDispatcher=useDispatcher )
        print "Returing wrapped", wrapped
        return wrapped

    def KissChild(self, child):
        print "KissChild called with child", child
        # Our child is a PyIDispatch object, so we will attempt
        # to use it as such.  To make it into something useful,
        # we must convert it to a win32com.client.Dispatch object.
        dispatch = win32com.client.Dispatch(child)
        print "KissChild called with child named", dispatch.Name

        # Now, assuming it is a Python child object, lets
        # unwrap it to get the object back!
        child = unwrap(child)
        print "The Python child is", child

# Our Child object.
# This is not registered        
class Child:
    _public_methods_ = []
    _public_attrs_ = ['Name']
    def __init__(self):
        self.Name = "Unnamed"

if __name__=='__main__':
    import win32com.server.register
    win32com.server.register.UseCommandLine(Parent, debug=debugging)
