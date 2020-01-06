# DumpPop2.py - Dumps and deletes a test message from a POP3 mailbox.
import sys
import poplib
import string
import mimetools
import cStringIO

def DumpAPopMessage(host, user, password):
    # Establish a connection to the POP server.
    a = poplib.POP3(host)
    # Note we print the server response, although not necessary!
    print a.user(user)
    print a.pass_(password)
    # The mailbox is now locked - ensure we unlock it!
    try:
        (numMsgs, totalSize) = a.stat()
        for thisNum in range(1, numMsgs+1):
            (server_msg, body, octets) = a.retr(1)
            # Create a file like object suitable for the
            # mimetools.Message class.
            pseudo_file = cStringIO.StringIO(string.join(body, '\n'))
            msg = mimetools.Message(pseudo_file)
            if msg.getheader("Subject")=="Hi from Python":
                print "Found our test message"
                print "Body is", `pseudo_file.read()`
                print a.dele(thisNum)
                print "Message deleted!"
    finally:
        print a.quit()

if __name__=='__main__':
    if len(sys.argv)<4:
        print "Usage:", sys.argv[0], "host username password"
    else:
        DumpAPopMessage(sys.argv[1], sys.argv[2], sys.argv[3])
