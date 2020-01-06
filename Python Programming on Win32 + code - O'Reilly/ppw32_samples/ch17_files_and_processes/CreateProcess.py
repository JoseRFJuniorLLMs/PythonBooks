# CreateProcess.py
#
# Demo of creating two processes using the CreateProcess API,
# then waiting for the processes to terminate.

import win32process
import win32event
import win32con
import win32api

# Create a process specified by commandLine, and
# The process' window should be at position rect
# Returns the handle to the new process.
def CreateMyProcess( commandLine, rect):
    # Create a STARTUPINFO object
    si = win32process.STARTUPINFO()
    # Set the position in the startup info.
    si.dwX, si.dwY, si.dwXSize, si.dwYSize = rect
    # And indicate which of the items are valid.
    si.dwFlags = win32process.STARTF_USEPOSITION | \
                 win32process.STARTF_USESIZE
    # Rest of startup info is default, so we leave it alone.
    # Create the process.
    info = win32process.CreateProcess(
                          None, # AppName
                          commandLine, # Command line
                          None, # Process Security
                          None, # ThreadSecurity
                          0, # Inherit Handles?
                          win32process.NORMAL_PRIORITY_CLASS,
                          None, # New environment
                          None, # Current directory
                          si) # startup info.
    # Return the handle to the process.
    # Recall info is a tuple of (hProcess, hThread, processId, threadId)
    return info[0]

def RunEm():
    handles = []
    # First get the screen size to calculate layout.
    screenX = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screenY = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    # First instance will be on the left hand side of the screen.
    rect = 0, 0, screenX/2, screenY
    handle = CreateMyProcess("notepad", rect)
    handles.append(handle)
    # Second instance of Notepad will be on the right hand side.
    rect = screenX/2+1, 0, screenX/2, screenY
    handle = CreateMyProcess("notepad", rect)
    handles.append(handle)

    # Now we have the processes, wait for them both
    # to terminate.
    # Rather than waiting the whole time, we loop 10 times,
    # waiting for one second each time, printing a message
    # each time around the loop
    countdown = range(1,10)
    countdown.reverse()
    for i in countdown:
        print "Waiting %d seconds for apps to close" % i
        rc = win32event.WaitForMultipleObjects(
                              handles, # Objects to wait for.
                              1, # Wait for them all
                              1000) # timeout in milli-seconds.
        if rc == win32event.WAIT_OBJECT_0:
            # Our processes closed!
            print "Our processes closed in time."
            break
        # else just continue around the loop.
    else:
        # We didn't break out of the for loop!
        print "Giving up waiting - killing processes"
        for handle in handles:
            try:
                win32process.TerminateProcess(handle, 0)
            except win32process.error:
                # This one may have already stopped.
                pass

if __name__=='__main__':
    RunEm()
