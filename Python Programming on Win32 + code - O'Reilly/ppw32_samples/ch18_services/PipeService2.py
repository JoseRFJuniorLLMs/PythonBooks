# PipeService2.py
#
# A sample demonstrating a service which uses a 
# named-pipe to accept client connections,
# and writes data to the event log.

import win32serviceutil
import win32service
import win32event
import win32pipe
import win32file
import pywintypes
import winerror
import perfmon
import os

class PipeService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PythonPipeService"
    _svc_display_name_ = "A sample Python service using named pipes"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        # We need to use overlapped IO for this, so we dont block when
        # waiting for a client to connect.  This is the only effective way
        # to handle either a client connection, or a service stop request.
        self.overlapped = pywintypes.OVERLAPPED()
        # And create an event to be used in the OVERLAPPED object.
        self.overlapped.hEvent = win32event.CreateEvent(None,0,0,None)
        # Finally initialize our Performance Monitor counters
        self.InitPerfMon()

    def InitPerfMon(self):
        # Magic numbers (2 and 4) must match header and ini file used
        # at install - could lookup ini, but then Id need it a runtime
        
        # A counter for number of connections per second.
        self.counterConnections=perfmon.CounterDefinition(2) 
        # We arent expecting many, so we set the scale high (ie, x10)
        # Note the scale is 10^DefaultScale = ie, to get 10, we use 1!
        self.counterConnections.DefaultScale = 1

        # Now a counter for the number of bytes received per second.
        self.counterBytes=perfmon.CounterDefinition(4)
        # A scale of 1 is fine for this counter.
        self.counterBytes.DefaultScale = 0

        # Now register our counters with the performance monitor
        perfObjectType = perfmon.ObjectType( 
                          (self.counterConnections, self.counterBytes) )
        
        self.perfManager = perfmon.PerfMonManager(
                        self._svc_name_,
                        (perfObjectType,),
                        "perfmondata")
                        
    def TermPerfMon(self):
        self.perfManager.Close()
        self.perfManager = None
    
    def SvcStop(self):
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # And set my event.
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        # Log a "started" message to the event log.
        import servicemanager
        servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE, 
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, ''))
                
        # We create our named pipe.
        pipeName = "\\\\.\\pipe\\PyPipeService"
        openMode = win32pipe.PIPE_ACCESS_DUPLEX | win32file.FILE_FLAG_OVERLAPPED
        pipeMode = win32pipe.PIPE_TYPE_MESSAGE
        
        # When running as a service, we must use special security for the pipe
        sa = pywintypes.SECURITY_ATTRIBUTES()
        # Say we do have a DACL, and it is empty
        # (ie, allow full access!)
        sa.SetSecurityDescriptorDacl ( 1, None, 0 )

        pipeHandle = win32pipe.CreateNamedPipe(pipeName,
            openMode,
            pipeMode,
            win32pipe.PIPE_UNLIMITED_INSTANCES,
            0, 0, 6000, # default buffers, and 6 second timeout.
            sa)

        # Loop accepting and processing connections
        while 1:            
            try:
                hr = win32pipe.ConnectNamedPipe(pipeHandle, self.overlapped)
            except error, details:
                print "Error connecting pipe!", details
                pipeHandle.Close()
                break
                   
            if hr==winerror.ERROR_PIPE_CONNECTED:
                # Client is fast, and already connected - signal event
                win32event.SetEvent(self.overlapped.hEvent)
            # Wait for either a connection, or a service stop request.
            timeout = win32event.INFINITE
            waitHandles = self.hWaitStop, self.overlapped.hEvent
            rc = win32event.WaitForMultipleObjects(waitHandles, 0, timeout)
            if rc==win32event.WAIT_OBJECT_0:
                # Stop event
                break
            else:
                # Pipe event - read the data, and write it back.
                # But first, increment our Performance Monitor data
                self.counterConnections.Increment()
                # (We only handle a max of 255 characters for this sample)
                try:
                    hr, data = win32file.ReadFile(pipeHandle, 256)
                    win32file.WriteFile(pipeHandle, "You sent me:" + data)
                    # And disconnect from the client.
                    win32pipe.DisconnectNamedPipe(pipeHandle)
                    # Update our performance monitor "bytes read" counter
                    self.counterBytes.Increment(len(data))

                    # Log a message to the event log indicating what we did.
                    message = "Processed %d bytes for client connection" % len(data)
                    servicemanager.LogInfoMsg(message)
                except win32file.error:
                    # Client disconnected without sending data
                    # or before reading the response.
                    # Thats OK - just get the next connection
                    continue

        # cleanup our PerfMon counters.
        self.TermPerfMon()

        # Now log a "service stopped" message
        servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE, 
                servicemanager.PYS_SERVICE_STOPPED,
                (self._svc_name_, ''))
                    
if __name__=='__main__':
    win32serviceutil.HandleCommandLine(PipeService)
