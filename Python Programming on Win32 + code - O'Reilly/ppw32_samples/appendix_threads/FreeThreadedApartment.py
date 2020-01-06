# FreeThreadedApartment.py
# Demonstrate the use of multiple threads all in the same
# multi-threading apartment.

# before the Pythoncom import, we specify free-threading.
import sys
sys.coinit_flags=0

from pythoncom import \
     CoInitializeEx, CoUninitialize, \
     COINIT_MULTITHREADED

from win32event import \
     WaitForMultipleObjects, \
     WAIT_ABANDONED

from win32com.client import Dispatch
from win32process import beginthreadex
from win32api import GetCurrentThreadId

def Demo( prog_id ):
    # First create the object
    object = Dispatch(prog_id)
    print "Thread", GetCurrentThreadId(), "creating object"
    created_id = object.GetCreatedThreadId()
    print "Object reports it was created on thread", created_id
    # Now create the threads, remembering the handles.
    handles = []
    for i in range(3):
        # Multi-threaded - just pass the objects directly to the thread.
        args = (object,)
        handle, id = beginthreadex(None, 0, WorkerThread, args, 0)
        handles.append(handle)
    # Now we have all the threads running, wait for them to terminate.
    # No need for message pump, so we can simply wait for all objects
    # in one call.
    rc = WaitForMultipleObjects(handles, 1, 5000)
    if rc == WAIT_ABANDONED:
        print "Gave up waiting for the threads to finish!"
    print "Demo of", prog_id, "finished."

def WorkerThread(object):
    # First step - initialize COM
    CoInitializeEx(COINIT_MULTITHREADED)
    this_id = GetCurrentThreadId()
    that_id = object.GetCurrentThreadId()
    message = "Thread is %d, and object is on thread %d" % \
                                     (this_id, that_id)
    print message
    # Be a good citizen and finalize COM, but
    # first remove our object references.
    object = None
    CoUninitialize()

if __name__=='__main__':
    print "Running Free threaded with Free Threaded object"
    Demo("PythonThreadDemo.Free")
