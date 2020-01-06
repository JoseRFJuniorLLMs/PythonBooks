# DumpStorage.py - Dumps some user defined properties 
# of a COM Structured Storage file.

import pythoncom
from win32com import storagecon # constants related to storage functions.

# These come from ObjIdl.h
FMTID_UserDefinedProperties = "{F29F85E0-4FF9-1068-AB91-08002B27B3D9}"

PIDSI_TITLE               = 0x00000002
PIDSI_SUBJECT             = 0x00000003
PIDSI_AUTHOR              = 0x00000004
PIDSI_CREATE_DTM          = 0x0000000c

def PrintStats(filename):
    if not pythoncom.StgIsStorageFile(filename):
        print "The file is not a storage file!"
        return
    # Open the file.
    flags = storagecon.STGM_READ | storagecon.STGM_SHARE_EXCLUSIVE
    stg = pythoncom.StgOpenStorage(filename, None, flags )

    # Now see if the storage object supports Property Information.
    try:
        pss = stg.QueryInterface(pythoncom.IID_IPropertySetStorage)
    except pythoncom.com_error:
        print "No summary information is available"
        return
    # Open the user defined properties.
    ps = pss.Open(FMTID_UserDefinedProperties)
    props = PIDSI_TITLE, PIDSI_SUBJECT, PIDSI_AUTHOR, PIDSI_CREATE_DTM
    data = ps.ReadMultiple( props )
    # Unpack the result into the items.
    title, subject, author, created = data
    print "Title:", title
    print "Subject:", subject
    print "Author:", author
    print "Created:", created.Format()

if __name__=='__main__':
    import sys
    if len(sys.argv)<2:
        print "Please specify a file name"
    else:
        PrintStats(sys.argv[1])
