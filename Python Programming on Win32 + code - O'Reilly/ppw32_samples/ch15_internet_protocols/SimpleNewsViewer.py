# SimpleNewsViewer.py

# Finds all news articles in a news group that have a specific word
# in its subject.  Then writes the results to a HTML file for
# easy reading.

# eg, running:
# c:\> SimpleNewsViewer.py comp.lang.python python 
#
# Will generate "comp.lang.python.html", and execute your 
# browser on this file. 

import sys, string

import nntplib

import win32api # to execute our browser.

g_newsserver = 'news-server.c3.telstra-mm.net.au'

def MakeNewsPage(groupname, subjectsearch, outfile ):
    print "Connecting..."
    nntp=nntplib.NNTP(g_newsserver)
    print "Fetching group information"
    # Most functions return the raw server response first.
    resp, numarts, first, last, name = nntp.group(groupname)
    # Get the subject line from these messages.
    print "Getting article information..."
    resp, data = nntp.xover(first, last)
    for artnum, subject, poster, time, id, references, size, numlines in data:
        # We will match on any case!
        subjectlook=string.lower(subject)
        if string.find(subjectlook, string.lower(subjectsearch))>=0:
            # Translate the "<" and ">" chars.
            subject = string.replace(subjectlook, "<", "&lt")
            poster = string.replace(poster, "<", "&lt")
            subject = string.replace(subject, ">", "&gt")
            poster = string.replace(poster, ">", "&gt")
            # Build a href
            href = "news:%s" % id[1:-1]
            # Write the HTML
            outfile.write('<P>From %s on %s<BR><a HREF="%s">%s</a>\n' \
                % (poster, time, href, subject))
    outfile.close()
    
if __name__=='__main__':
    if len(sys.argv)<3:
        print "usage: %s groupname, searchstring" % sys.argv[0]
        sys.exit(1)
    
    groupname = sys.argv[1]
    search = sys.argv[2]
    outname = groupname + ".htm"

    # Open the outfile file.
    outfile = open(outname, "w")

    MakeNewsPage(groupname, search, outfile)
    print "Done - Executing", outname
    win32api.ShellExecute(0, "open", outname, None, "", 1)
