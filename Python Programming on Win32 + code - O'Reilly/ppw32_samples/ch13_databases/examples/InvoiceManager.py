# InvoiceManager.py
# - builds object layers on top of databases.

DATASOURCE = 'PYDBDEMOS'   # put your alias here
USERID = 'Admin'     # default for all access databases
PWD = ''             # default for access databases

import ODBC.Windows
import pprint
pp = pprint.pprint   # pretty-print - save some typing

class InvoiceManager:
    "Keeps a list of customers, indexed by InvoiceID"
    
    def connect(self):
        self.conn = ODBC.Windows.Connect(DATASOURCE,user=USERID,password=PWD)
        
    def test(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * from Clients')
        pp(cursor.fetchall())
        
    def __del__(self):
        self.conn.close()


def test():
    mgr = InvoiceManager()
    mgr.connect()
    mgr.test()
            