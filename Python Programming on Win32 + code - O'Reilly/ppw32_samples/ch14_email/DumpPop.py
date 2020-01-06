# DumpPop.py - Dumps the first message in a POP3 mailbox.
import sys
import poplib

def DumpAPopMessage(host, user, password):
    # Establish a connection to the POP server.
    a = poplib.POP3(host)
    # Note we print the server response, although not necessary!
    print a.user(user)
    print a.pass_(password)
    # The mailbox is now locked - ensure we unlock it!
    try:
        (numMsgs, totalSize) = a.stat()
        if numMsgs == 0:
            print "Sorry - there are no messages in the mailbox"
        else:
            (server_msg, body, octets) = a.retr(1)
            print "Server Message:", server_msg
            print "Number of Octets:", octets
            print "Message body:"
            for line in body:
                print line
    finally:
        print a.quit()

if __name__=='__main__':
    if len(sys.argv)<4:
        print "Usage:", sys.argv[0], "host username password"
    else:
        DumpAPopMessage(sys.argv[1], sys.argv[2], sys.argv[3])
