# Utility functions for chapter 14

import time, string

def hhmm_to_seconds(hhmm):
    hh,mm = hhmm[:2], hhmm[2:]
    return 360*string.atoi(hh) + 60*string.atoi(mm)

def get_hhmm(t):
    tuple = time.localtime(t)
    minutes = tuple[3]*100 + tuple[4] +10000
    return str(minutes)[1:]

