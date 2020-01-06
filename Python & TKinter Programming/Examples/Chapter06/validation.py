from tkMessageBox import *
import string

def validIP(value):
    valid = 0
    try:
        if len(value) >=7 and len(value) <= 15:
            fields = string.splitfields(value, '.')
            if len(fields) < 5:
                for field in fields:
                    iV = string.atoi(field)
                    if iV < 0 or iV > 255:
                        valid = 0
                        break
                    else:
                        valid = 1
    except:
        pass
    if not valid:
        showerror(title='Invalid IP Address',
                  message='Format: nnn.nnn.nnn.nnn\n-1 < nnn < 256')
    return (value, 0, valid)

def validCP(value):
    valid = 0
    try:
        fields = string.splitfields(value, '-')
        for field in fields:
            iV = string.atoi(field)
            if iV < 1 or iV > 100:
                valid = 0
                break
            else:
                valid = 1
    except:
        pass
    if not valid:
        showerror(title='Invalid Card-Port',
                  message='Format: nnn-nnn\n0 < nnn < 101'),
    return (value, 0, valid)

def validLName(value):
    valid = 0
    try:
        if len(value) >= 3:
            ucFTC = string.upper(value[:2])
            if ucFTC == 'CP':
                valid = 1
    except:
        pass
    if valid:
        retval = 'CP' + value[2:]
        replace = 1
    else:
        showerror(title='Invalid Logical Name',
                  message='Format: CP+<text>')
        retval = value
        replace = 0
    return (retval, replace, valid)
