# serial.py

"""Win32 serial port interface.

   Serial Communications DLLs (Wsc32.dll) by
   MarshallSoft Computing, Inc.
   POB 4543 Huntsville AL 35815. 205-881-4630.
   Email: mike@marshallsoft.com

   This module wraps the shared library Sio.pyd which
   provides access to the Wsc32.dll.

   This module exports classes:

      PortDict - manages port parameters, looks like a dictionary
      Port     - wrap access to the Sio functions

   And will raise SioError exceptions.

   These constants are exported:
      RSP_NONE, RSP_TERMINATED, RSP_FIXEDLEN, RSP_BEST_EFFORT,
      COM1, ..., COM9,
      Baud110, Baud300, Baud1200, Baud2400, Baud4800, Baud9600, Baud19200,
         Baud38400, Baud57600, Baud115200,
      NoParity, OddParity, EvenParity, MarkParity, SpaceParity,
      OneStopBit, TwoStopBits
      WordLength5, WordLength6, WordLength7, WordLength8

"""


import sys
import regex
import string
from types import IntType, StringType
from mstimer import MsTimer
from crilib import *
from sio import *


[RSP_NONE, RSP_TERMINATED, RSP_FIXEDLEN, RSP_BEST_EFFORT] = range(0, 4)
PORT_CLOSED = -1


class PortDict:

    """A dictionary used to parameterize a Port object.

    Usage:  import serial
        d = serial.PortDict()
        d['port'] = serial.COM2
        ...
        fd = serial.Port()
        fd.open(d)

    Entries (keys are all strings):
        debug:        Boolean, turn on/off debug/tracing
        port:         Port param COM1 ... Com9
        baud:         Port param, Baud110|Baud300|Baud1200|Baud2400|Baud4800
                      |Baud9600|Baud19200|Baud38400|Baud57600|Baud115200
        parity:       Port param, NoParity|OddParity|EvenParity|MarkParity
                      |SpaceParity 
        stopBits:     Port param, OneStopBit|TwoStopBits
        dataBits:     Port param, WordLength5|WordLength6|WordLength7
                      |WordLength8
        rxBufSize:    Maximum size of a rsp
        rxBufSize:    Maximum size of a cmd
        timeoutMs:    Milliseconds to wait for expected responses
        cmdsEchoed:   Boolean, whether hdw echoes characters or not
        cmdTerm:      String expected to terminate RSP_TERMINATED command
                      responses
        rspTerm:      String appended to cmd's
        rspType:      Used by cmd methods, RSP_NONE|RSP_TERMINATED|RSP_FIXEDLEN
                      |RSP_BEST_EFFORT
        rspFixedLen:  Length of expected rsp, if rspType == RSP_FIXEDLEN
        rtsSignal     RTS signal setting (S set or C clear)
        dtrSignal     DTR signal setting (S set or C clear)        

    """

    portKw = {
        COM1: 'COM1',
        COM2: 'COM2',
        COM3: 'COM3',
        COM4: 'COM4',
        COM5: 'COM5',
        COM6: 'COM6',
        COM7: 'COM7',
        COM8: 'COM8',
        COM9: 'COM9'
        }
    baudKw = {
        Baud110: 'Baud110',
        Baud300: 'Baud300',
        Baud1200: 'Baud1200',
        Baud2400: 'Baud2400',
        Baud4800: 'Baud4800',
        Baud9600: 'Baud9600',
        Baud19200: 'Baud19200',
        Baud38400: 'Baud38400',
        Baud57600: 'Baud57600',
        Baud115200: 'Baud115200'
        }
    parityKw = {
        NoParity: 'NoParity',
        OddParity: 'OddParity',
        EvenParity: 'EvenParity',
        MarkParity: 'MarkParity',
        SpaceParity: 'SpaceParity'
        }
    stopBitsKw = {
        OneStopBit: 'OneStopBit',
        TwoStopBits: 'TwoStopBits'
        }
    dataBitsKw = {
        WordLength5: 'WordLength5',
        WordLength6: 'WordLength6',
        WordLength7: 'WordLength7',
        WordLength8: 'WordLength8'
        }
    rspTypeKw = {
        RSP_NONE: 'RSP_NONE',
        RSP_TERMINATED: 'RSP_TERMINATED',
        RSP_FIXEDLEN: 'RSP_FIXEDLEN',
        RSP_BEST_EFFORT: 'RSP_BEST_EFFORT'
        }
    paramKws = {
        'port': portKw,
        'baud': baudKw,
        'parity': parityKw,
        'stopBits': stopBitsKw,
        'dataBits': dataBitsKw,
        'rspType': rspTypeKw
        }

    portVals = tuple(portKw.keys())
    baudVals = tuple(baudKw.keys())
    parityVals = tuple(parityKw.keys())
    stopBitVals = tuple(stopBitsKw.keys())
    dataBitVals = tuple(dataBitsKw.keys())
    rspTypeVals = tuple(rspTypeKw.keys())
    
    def __init__(self):
        """Create a serial port configuration dictionary that can be modified
        before passing to the Port.open method.

        """
        self._dict = {}
        self._dict['debug'] = FALSE
        self._dict['port'] = COM2
        self._dict['baud'] = Baud9600
        self._dict['parity'] = NoParity
        self._dict['stopBits'] = OneStopBit
        self._dict['dataBits'] = WordLength8
        self._dict['rxBufSize'] = 1024
        self._dict['txBufSize'] = 1024
        self._dict['timeOutMs'] = 500
        self._dict['cmdsEchoed'] = FALSE
        self._dict['cmdTerm'] = ''
        self._dict['rspTerm'] = ''
        self._dict['rspTermPat'] = None
        self._dict['rspType'] = RSP_BEST_EFFORT
        self._dict['rspFixedLen'] = 0
        self._dict['rtsSignal'] = 'S'
        self._dict['dtrSignal'] = 'S'

    def __getitem__(self, key):
        """Normal dictionary behavior."""
        return self._dict[key]

    def __setitem__(self, key, value):
        """Only allow existing items to be changed.  Validate entries"""
        if self._dict.has_key(key):
            if key == 'port':
                if not value in PortDict.portVals:
                    raise AttributeError, 'Illegal port value'
            elif key == 'baud':
                if not value in PortDict.baudVals:
                    raise AttributeError, 'Illegal baud value'
            elif key == 'parity':
                if not value in PortDict.parityVals:
                    raise AttributeError, 'Illegal parity value'
            elif key == 'stopBits':
                if not value in PortDict.stopBitVals:
                    raise AttributeError, 'Illegal stopBits value'
            elif key == 'dataBits':
                if not value in PortDict.dataBitVals:
                    raise AttributeError, 'Illegal dataBits value'
            elif key == 'rspType':
                if not value in PortDict.rspTypeVals:
                    raise AttributeError, 'Illegal rspType value'
            elif key == 'rxBufSize' or key == 'txBufSize':
                if value <= 0:
                    raise AttributeError, 'buffer size must be > 0'
            elif key == 'timeOutMs':
                if value <= 0 or value > 60000:
                    raise AttributeError, '0 < timeOutMs <= 60000'
            elif key == 'cmdTerm' or key == 'rspTerm':
                if type(value) != StringType:
                    raise AttributeError, 'terminators must be strings'
            elif key == 'rspTermPat':
                raise AttributeError, 'cannot set rspTermPat directly,'\
                      'store rspTerm instead'
            elif key == 'rspFixedLen':
                if value <= 0 or value > self._dict['rxBufSize']:
                    raise AttributeError, \
                          '0 < rspFixedLen <= %d' % self._dict['rxBufSize']
            elif key == 'debug' or key == 'cmdsEchoed':
                if type(value) != IntType:
                    raise AttributeError, 'must be a boolean value'
            elif key == 'rtsSignal':
                if not value[:1] in 'CS':
                     raise AttributeError, 'Illegal rtsSignal value'
            elif key == 'dtrSignal':
                if not value[:1] in 'CS':
                     raise AttributeError, 'Illegal dtrSignal value'
               
            self._dict[key] = value
            if key == 'rspTerm':
                self._dict['rspTermPat'] = regex.compile('^.*%s$' % value)
        else:
            raise KeyError, 'No such key %s in a PortDict' % key

    def has_key(self, key):
        """Normal dictionary behavior."""
        return self._dict.has_key(key)

    def keys(self):
        """Normal dictionary behavior."""
        return self._dict.keys()

    def __repr__(self):
        """Format a listing of current options."""
        str = '<serial Config:'
        keys = self._dict.keys()
        keys.sort()
        for k in keys:
            if PortDict.paramKws.has_key(k):
                d = PortDict.paramKws[k]
                str = str + '\n   %s = %s' % (k, d[self._dict[k]])
            else:
                str = str + '\n   %s = %s' % (k, `self._dict[k]`)
        str = str + '\n>\n'
        return str


class Port:

    """Encapsulate methods for accessing the Win32 serial ports.

    Public methods:
       open(cfg) -- Open port specified by PortDict instance cfg.

       flush()  -- Empty receive and transmit buffers.

       getLastFlush() -- Return the last string that was flushed.

       getLastRsp()  -- Return the last response.

       close() -- Close the connection.

       write(str, cnt=None) -- Write cnt (len(str), if cnt=None) 
       bytes of str to port.

       writeVerifyEcho(str, cnt=None) -- sSame as write, but verify 
       each chr was echoed.

       read(cnt=None, timed=FALSE) -- Try to return cnt bytes read from port
       (cnt==None, read whatever is there, cnt!=None & timed==TRUE, then read 
       must complete in configured timeOutMs time).

       readTerminated() -- Read from port until terminator string read.
       Must complete within timeOutMs, return string minus the terminator.

       cmd(str='') -- Write or writeVerifyEcho str, then read till rspType
       satisfied, or times out.

"""

    def __init__(self):
        """Instance created, but not attached to any port."""
        self.debug = FALSE
        self.port = PORT_CLOSED
        self.cfg = {}
        self._rsp = ''
        self._bufSize = 0
        self._flushed = ''

    def _trace(self, tag, msg=''):
        """If debugging enabled, print a message"""
        if self.debug:
            print 'Port.%s: %s' % (tag, msg)

    def _chkSioExec(self, func, args):
        """Execute an sio function, raise SioError on negative return value."""
        status = apply(func, args)
        self._trace('_chkSioExec', '%s = %s%s' \
                    % (`status`, func.__name__, `args`))
        if status < 0:
            raise SioError, func.__name__ + ': ' + SioErrorText(status)
        return status

    def open(self, cfg):
        """Attach to the port specified in the cfg arg, then:
        
        -Open the port, set baud, parity, stopBits, and dataBits as per cfg.
        -Clear xmit/rec buffers, enable DTR, RTS, disable flow ctl.

        """
        self.debug = cfg['debug']
        self._trace('open')
        if self.port >= 0:
            raise SioError, 'Port is already open'
        port = cfg['port']
        self.cfg = cfg
        self._bufSize = cfg['rxBufSize']
        self._chkSioExec(SioReset, (port, self._bufSize, cfg['txBufSize']))
        self._chkSioExec(SioBaud, (port, cfg['baud']))
        self._chkSioExec(SioParms, (port, cfg['parity'], cfg['stopBits'], 
                                    cfg['dataBits']))
        self._chkSioExec(SioTxClear, (port,))
        self._chkSioExec(SioRxClear, (port,))
        self._chkSioExec(SioDTR, (port, cfg['dtrSignal'][:1]))
        self._chkSioExec(SioRTS, (port, cfg['rtsSignal'][:1]))
        self._chkSioExec(SioFlow, (port, 'N'))
        self.port = port
        self._rsp = ''
        self._flushed = ''

    def flush(self):
        """Save any pending input in _flushed; clear xmit/rec bufs."""
        self._trace('flush')
        self._flushed = ''
        self._flushed = SioGets(self.port, self._bufSize)
        self._chkSioExec(SioTxClear, (self.port,))
        self._chkSioExec(SioRxClear, (self.port,))
        self._trace('flushed', '|%s|' % self._flushed)

    def getLastFlush(self):
        """Return the last contents of the flushed buffer."""
        return self._flushed[:]

    def getLastRsp(self):
        """Return the last contents of the response buffer."""
        return self._rsp[:]
   
    def close(self):
        """Close the port."""
        self._trace('close')
        self._chkSioExec(SioDone, (self.port,))
        self.port = PORT_CLOSED

    def write(self, str, cnt=None):
        """Write cnt bytes of str out port, cnt defaults to len(str)."""
        self._trace('write')
        if cnt is None:
            cnt = len(str)
        elif cnt > len(str):
            raise SioError, 'write: request to send more bytes than in the str'
        self.flush()
        self._chkSioExec(SioPuts, (self.port, str, cnt))

    def writeVerifyEcho(self, str, cnt=None):
        """Same as write , but verify each char was echoed by the hdw. """
        self._trace('writeVerifyEcho')
        if cnt is None:
            cnt = len(str)
        elif cnt > len(str):
            raise SioError, \
                  'writeVerifyEcho: request to send more bytes than in the str'
        i = 0
        self.flush()
        elapsed = MsTimer()
        timeOut = self.cfg['timeOutMs']
        msecs = 0
        while i < cnt:
            sent = str[i]
            self._chkSioExec(SioPutc, (self.port, sent))
            elapsed.reset()
            while 1:
                got = SioGetc(self.port)
                gotChr = '%c' % got
                msecs = elapsed()
                if got == WSC_NO_DATA:
                    if msecs >= timeOut:
                        raise SioError, \
                              'Timed out waiting for chr %d of cmd %s to echo'\
                              % (i, `str`)
                elif got < 0:
                    raise SioError, SioGetc.__name__ + ': ' + SioErrorText(got)
                elif gotChr <> sent:
                    raise SioError, \
                          'writeVerifyEcho: Bad echo of chr %i in cmd %s:'\
                          'sent %s, got %s' % (i, `str`, `sent`, `gotChr`)
                else:
                    self._trace('writeVerifyEcho', 'waited %d mSecs' % msecs)
                    self._trace('writeVerifyEcho', '%s = SioGetc(%d)' \
                                % (`gotChr`, self.port))
                    break
            i = i + 1

    def read(self, cnt=None, timed=FALSE):
        """Attempt to read cnt bytes, if timed TRUE, must complete in cfg time.
        """
        self._trace('read')
        if cnt is None:
            cnt = self._bufSize
        if cnt < 0: cnt = 0
        if not timed:
            self._rsp = SioGets(self.port, cnt)
        else:
            timeOut = self.cfg['timeOutMs']
            buf = ''
            got = 0
            elapsed = MsTimer()
            while 1:
                thisCnt = cnt - got
                thisBuf = SioGets(self.port, thisCnt)
                thisGot = len(thisBuf)
                buf = buf + thisBuf
                got = got + thisGot
                if got < cnt:
                    msecs = elapsed()
                    if msecs >= timeOut:
                        self._rsp = buf
                        raise SioError, \
                              'Timed out waiting for input chr %d of %d, '\
                              'read %s' % (got, cnt, `buf`)
                else:
                    self._rsp = buf
                    break
        return self._rsp[:]

    def readTerminated(self):
        """Read from port until terminator read, timed out, or buf overflow.
        Terminator is stripped off of result."""
        self._trace('readTerminated')
        timeOut = self.cfg['timeOutMs']
        patLen = len(self.cfg['rspTerm'])
        pat = self.cfg['rspTermPat']
        if patLen <= 0 or pat is None:
            raise SioError, 'Config rspTerm is empty, can not readTerminated'
        i = 0
        buf = ''
        elapsed = MsTimer()
        msecs = 0
        while 1:
            got = SioGetc(self.port)
            gotChr = '%c' % got
            msecs = elapsed()
            if got == WSC_NO_DATA:
                if msecs >= timeOut:
                    self._rsp = buf
                    raise SioError, \
                          'Timed out waiting for chr %d of input, read %s' \
                          % (i, `buf`)
            elif got < 0:
                self._rsp = buf
                raise SioError, SioGetc.__name__ + ': ' + SioErrorText(got)
            elif i == self._bufSize:
                self._rsp = buf
                raise SioError, \
                      'Buffer overrun getting terminated input, read %s' \
                      % `buf`
            else:
                self._trace('readTerminated', 'waited %d mSecs' % msecs)
                self._trace('readTerminated', '%s = SioGetc(%d)' \
                            % (`gotChr`, self.port))
                buf = buf + gotChr
                i = i + 1
                if pat.search(buf) >= 0:
                    buf = buf[:-patLen]
                    break
        self._rsp = buf
        return self._rsp[:]

    def cmd(self, str=''):
        """Send a str, get a rsp according to cfg."""
        self._trace('cmd')
        rspType = self.cfg['rspType']

        if rspType == RSP_NONE:
            pass
        elif rspType == RSP_TERMINATED:
            if len(self.cfg['rspTerm']) <= 0:
                raise SioError, \
                      'Config param rspTerm is empty, can not readTerminated'
        elif rspType == RSP_FIXEDLEN:
            fixLen = self.cfg['rspFixedLen']
            if fixLen <= 0:
                raise SioError, \
                      'Config param rspFixedLen is <= 0, can not read '\
                      'fixed length reply'
        elif rspType == RSP_BEST_EFFORT:
            pass

        cmdStr = str + self.cfg['cmdTerm']
        rsp = ''

        if self.cfg['cmdsEchoed']:
            self.writeVerifyEcho(cmdStr)
        else:
            self.write(cmdStr)

        if rspType == RSP_NONE:
            pass
        elif rspType == RSP_TERMINATED:
            rsp = self.readTerminated()
        elif rspType == RSP_FIXEDLEN:
            rsp = self.read(cnt=fixLen)
        elif rspType == RSP_BEST_EFFORT:
            rsp = self.read()

        self._rsp = rsp
        return self._rsp[:]

