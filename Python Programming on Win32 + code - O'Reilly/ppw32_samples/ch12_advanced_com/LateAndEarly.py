# LateAndEarly.py - Demonstrates how to force
# late or early binding of your COM objects.

import win32com.client
import win32com.client.dynamic

print "Creating late-bound Excel object"
xl = win32com.client.dynamic.Dispatch("Excel.Application")
print "The Excel object is", `xl`


print "Running makepy for Excel"
# NOTE - these 2 lines are copied verbatim from the output
# of makepy.py when run with the -i parameter.
from win32com.client import gencache
gencache.EnsureModule('{00020813-0000-0000-C000-000000000046}', 0, 1, 2)

xl = win32com.client.Dispatch("Excel.Application")
print "The Excel object is", `xl`

