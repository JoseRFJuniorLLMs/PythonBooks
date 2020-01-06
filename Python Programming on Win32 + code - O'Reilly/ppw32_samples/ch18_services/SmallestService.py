# SmallestService.py
#
# A sample demonstrating the smallest possible service written in Python.

import win32serviceutil
import win32service
import win32event

class SmallestPythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SmallestPythonService"
    _svc_display_name_ = "The smallest possible Python Service"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # And set my event.
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        # We do nothing other than wait to be stopped!
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(SmallestPythonService)
