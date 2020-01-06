#!/usr/bin/env python
import dbapi20
import unittest
import MySQLdb

class test_MySQLdb(dbapi20.DatabaseAPI20Test):
    driver = MySQLdb
    connect_args = ()
    connect_kw_args = {'db': 'test', 'read_default_file': '~/.my.cnf'}

    def test_setoutputsize(self): pass
    def test_setoutputsize_basic(self): pass
    def test_nextset(self): pass
    
if __name__ == '__main__':
    unittest.main()
