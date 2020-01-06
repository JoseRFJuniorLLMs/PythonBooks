# laundry.py
from string import join
from pprint import pprint
import ODBC.Windows
import DateTime

class Record:
    #holds arbitrary database data
    def __init__(self):
        self._dbdata = {}
        
    def loadFromDict(self, aDict):
        "accept all attributes in the dictionary"
        self._dbdata.update(aDict)

    def getData(self):
        return self._dbdata.copy()
        
    def pp(self):
        "pretty-print my database data"
        pprint(self._dbdata)
        
    def __getattr__(self, key):
        """This is called if the object lacks the attribute.
        If the key is not found, it raises an error in the
        same way that the attribute access would were no
        __getattr__ method present.  """
        return self._dbdata[key]
    
            
        
class Customer(Record):
    def __getattr__(self, key):
        #trap attempts to fetch the list of invoices
        if key == 'Invoices':
            self.fetchInvoices()
            return self.Invoices
        else:
            #now call the inherited method
            return Record.__getattr__(self, key)

    def fetch(self, conn, key):
        self.conn = conn
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE ClientID = '%s'" % key)
        dicts = DataSetFromCursor(cursor).asDicts()
        assert len(dicts) == 1, 'Error fetching data!'
        self.loadFromDict(dicts[0])
        
    def fetchInvoices(self):
        #presumes an attribute pointing to the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Invoices WHERE ClientID = '%s'" % self.ClientID)
        ds = DataSetFromCursor(cursor)
        self.Invoices = ds.asObjects()        
    
        
    


def getFieldNames(cursor):
    "Extracts the fieldnames from the cursor"
    result= []
    for fieldinfo in cursor.description:
        result.append(fieldinfo[0])
    return tuple(result)
    
def dictToInsert(dict, tablename):
    "returns an INSERT statement"
    db_keys = []
    db_values = []
    for (key, value) in dict.items():
        typ = type(value)
        if value == None:
            continue
        elif typ == DateTime.DateTimeType:
            db_values.append(repr(value.COMDate()))
        else:
            db_values.append(repr(value))
        db_keys.append(key)
    stmt = 'INSERT INTO %s (%s) VALUES (%s);' % (
                    tablename,
                    join(db_keys, ','),
                    join(db_values, ',')
                    )
    return stmt



class DataSet:
    "Cut-down demo illusrating general principles; add methods as needed"
    def __init__(self):
        self.data = []
        self.fieldnames = []
        
    def pp(self):
        "Pretty-print a row at a time - nicked from Gadfly"
        from string import join
        stuff = [repr(self.fieldnames)] + map(repr, self.data)
        print join(stuff, "\n")
        
    def asDicts(self):
        "returns a list of dictionaries, each with all fieldnames"
        dicts = []
        fieldcount = len(self.fieldnames)
        for row in self.data:
            dict = {}
            for i in range(fieldcount):
                dict[self.fieldnames[i]] = row[i]
            dicts.append(dict)
        return dicts
    
    def asObjects(self):
        dicts = self.asDicts()
        objects = []
        for dict in dicts:
            obj = Record()
            obj.loadFromDict(dict)
            objects.append(obj)
        return objects        
            
    def detabulate(self):
        # returns a new dataset; categories in column 1
        colcount = len(self.fieldnames) - 1            
        rowcount = len(self.data) - 1
        assert colcount>1, 'Not enough columns'
        result = DataSet()
        result.fieldnames = ['Row','Column','Value']
        for col in range(colcount):
            colkey = self.fieldnames[col+1]
            for row in self.data:
                rowkey = row[0]
                value = row[col+1]
                result.data.append((rowkey, colkey, value))
        return result

    def addColumn(self, fieldname, valuelist, position=None):
        "Inserts a new column"
        if position is None:
            position = len(self.fieldnames)
        newnames = list(self.fieldnames) 
        newnames.insert(position, fieldname)
        newrows = []
        for i in range(len(self.data)):
            newrow = list(self.data[i])
            newrow.insert(position, valuelist[i])
            newrows.append(tuple(newrow))
        self.fieldnames = tuple(newnames)
        self.data = newrows
    
    def addConstantColumn(self, fieldname, value, position=None):
        values = [value] * len(self.data)
        self.addColumn(fieldname, values, position)
    
def DataSetFromCursor(cursor):
    ds = DataSet()
    ds.fieldnames = getFieldNames(cursor)
    ds.data = cursor.fetchall()
    return ds

def DataSetFromDicts(dictlist, keylist=None):
    #tabulates shared keys
    if not keylist:   # take all the keys
        all_key_dict = dictlist[0]
        for dict in dictlist:
            all_key_dict.update(dict)
        keylist = all_key_dict.keys()
        keylist.sort()  # better than random order
    ds = DataSet()
    ds.fieldnames = tuple(keylist)
    for dict in dictlist:    # loop over rows
        row = []   
        for key in keylist:  # loop over fields
            try:
                value = dict[key]
            except:
                value = None
            row.append(value)
        ds.data.append(tuple(row))
    return ds
    

def getFigure4Data():
        # an example for the book
        ds = DataSet()
        ds.fieldnames = ('Patient','X','Y','Z')
        ds.data = [
                ('Patient 1', 0.55, 0.08, 0.97),
                ('Patient 2', 0.54, 0.11, 0.07),
                ('Patient 3', 0.61, 0.08, 0.44),
                ('Patient 4', 0.19, 0.46, 0.41)
                ]
        return ds
 

    
def getadict():
    # gives us one row for testing    
    conn = ODBC.Windows.Connect('PYDBDEMOS')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Invoices')
    ds = DataSetFromCursor(cursor)
    cursor.close()
    conn.close()
    return ds.asDicts()[0]    
    
    
def test():
    conn = ODBC.Windows.Connect('PYDBDEMOS')
    # for normal ODBC module use:
    # import dbi, odbc
    # conn = odbc.odbc('PYDBDEMOS')

    cursor = conn.cursor()
    cursor.execute('SELECT ClientID, PeriodEnding, Consultant, Hours FROM Invoices')
    
    print 'Executed query'    
    ds = DataSetFromCursor(cursor)
    cursor.close()
    conn.close()
    
    print 'DataSet built:'
    ds.pp()
    
    dicts = ds.asDicts()
    print 'Dictionaries built.  First one is:'
    pprint(dicts[0])
    
    return dicts
