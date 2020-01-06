# SingleThreadedApartment.py
# Demonstrate the use of multiple threads, each in their own
# single-threaded apartment.

# As we do not set sys.coinit_flags=0
# before the Pythoncom import, Python
# initializes the main thread for single threading.
from pythoncom import \
     CoInitialize, CoUninitialize, IID_IDispatch,\
     CoMarshalInterThreadInterfaceInStream, \
     CoGetInterfaceAndReleaseStream, \
     PumpWaitingMessages

from win32event import \
     MsgWaitForMultipleObjects, \
     QS_ALLINPUT, WAIT_TIMEOUT, WAIT_OBJECT_0

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
        # As we are not allowed to pass the object directly between
        # apartments, we need to marshal it.
        object_stream = CoMarshalInterThreadInterfaceInStream(
                          IID_IDispatch, object )
        # Build an argument tuple for the thread.
        args = (object_stream,)
        handle, id = beginthreadex(None, 0, WorkerThread, args, 0)
        handles.append(handle)
    # Now we have all the threads running, wait for them to terminate.
    # also remember how many times we are asked to pump messages.
    num_pumps = 0
    while handles:
        # A quirk in MsgWaitForMultipleObjects means we must wait
        # for each event one at at time
        rc = MsgWaitForMultipleObjects(handles, 0, 5000, QS_ALLINPUT)
        if rc >= WAIT_OBJECT_0 and rc < WAIT_OBJECT_0+len(handles):
            # A thread finished - remove its handle.
            del handles[rc-WAIT_OBJECT_0]
        elif rc==WAIT_OBJECT_0 + len(handles):
            # Waiting message
            num_pumps = num_pumps + 1
            PumpWaitingMessages()
        else:
            print "Nothing seems to be happening",
            print "but I will keep waiting anyway..."
    print "Pumped messages", num_pumps, "times"
    print "Demo of", prog_id, "finished."

def WorkerThread(object_stream):
    # First step - initialize COM
    CoInitialize() # Single-threaded.
    # Unmarshal the IDispatch object.
    object = CoGetInterfaceAndReleaseStream(
        object_stream, IID_IDispatch)
    # The object we get back is a PyIDispatch, rather
    # than a friendly Dispatch instance, so we convert
    # to a usable object.
    object = Dispatch(object)
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
    print "Running with Apartment Threaded object"
    Demo("PythonThreadDemo.Apartment")
    print
    print "Running with Free Threaded object"
    Demo("PythonThreadDemo.Free")
