# CheckFileSemantics.py
#    Demonstrate the semantics of CreateFile.

# To keep the source code small, 
# we import all win32file objects.
from win32file import *

import win32api
import os

# First, lets create a normal file
h1 = CreateFile( \
       "\\file1.tst", # The file name \
       GENERIC_WRITE, # we want write access. \
       FILE_SHARE_READ, # others can open for read \
       None, # No special security requirements \
       CREATE_ALWAYS, # File to be created. \
       FILE_ATTRIBUTE_NORMAL, # Normal attributes \
       None ) # No template file.

# now we will print the handle, 
# just to prove we have one!
print "The first handle is", h1

# Now attempt to open the file again, 
# this time for read access
h2 = CreateFile( \
      "\\file1.tst", # The same file name. \
      GENERIC_READ, # read access \
      FILE_SHARE_WRITE | FILE_SHARE_READ, \
      None, # No special security requirements \
      OPEN_EXISTING, # expect the file to exist. \
      0, # Not creating, so attributes dont matter. \
      None ) # No template file

# Prove we have another handle
print "The second handle is", h2

# Now attempt yet again, but for write access.
# We expect this to fail.
try:
  h3 = CreateFile( \
        "\\file1.tst", # The same file name. \
        GENERIC_WRITE, # write access \
        0, # No special sharing \
        None, # No special security requirements \
        CREATE_ALWAYS, # attempting to recreate it! \
        0, # Not creating file, so no attributes  \
        None ) # No template file

except win32api.error, (code, function, message):
  print "The file could not be opened for write mode."
  print "Error", code, "with message", message

# Close the handles.
h1.Close()
h2.Close()

# Now lets check out the FILE_FLAG_DELETE_ON_CLOSE
fileAttributes = FILE_ATTRIBUTE_NORMAL | \
                 FILE_FLAG_DELETE_ON_CLOSE

h1 = CreateFile( \
       "\\file1.tst", # The file name \
       GENERIC_WRITE, # we want write access. \
       FILE_SHARE_READ, # others can open for read \
       None, # no special security requirements \
       CREATE_ALWAYS, # file to be created. \
       fileAttributes, \
       None ) # No template file.

# Do a stat of the file to ensure it exists.
print "File stats are", os.stat("\\file1.tst")

# Close the handle
h1.Close()

try:
	os.stat("\\file1.tst")
except os.error:
	print "Could not stat the file - file does not exist"

