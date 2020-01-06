ADOsession = """
>>> import win32com.client
>>> adoConn = win32com.client.Dispatch('ADODB.Connection')
>>> adoConn.Open('PYDBDEMOS')  # use our ODBC alias again
>>> (adoRS, success) = adoConn.Execute('SELECT * FROM Clients')
>>> adoRS.MoveFirst()
>>> adoRS.Fields("CompanyName").Value
'MegaWad Investments'
>>> adoConn = win32com.client.Dispatch('ADODB.Connection')
>>> adoConn.Open('PYDBDEMOS')  # use our ODBC alias again
>>> (adoRS, success) = adoConn.Execute('SELECT * FROM Clients')
>>> import os
os.chdir('c:\\data\\project\\oreilly\\ch13_databases\\examples')

>>> adoRS = win32com.client.Dispatch('ADODB.Recordset')
>>> adoConn = win32com.client.Dispatch('ADODB.Connection')
>>> adoConn.Open('PYDBDEMOS')
>>> from win32com.client import constants
>>> adoRS.Open('SELECT * FROM Invoices',
... 	adoConn,
... 	constants.adOpenKeyset,
... 	constants.adLockBatchOptimistic
... 	)
... 	
>>> # now we have a batch cursor
>>> 
"""