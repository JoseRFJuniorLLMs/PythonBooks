# -*- Mode: Python; tab-width: 4 -*-

# Create a new Jet database via the ODBC installer DLL.

# A note on an interesting 'hack' using the Jet ODBC driver: CREATE
# VIEW (though undocumented) actually works, and will create a new
# query object in the database which you can then examine/edit from
# the UI.  Not sure about updatable views/queries, though.

import os
import regsub

#from dyn_win32 import odbc_installer, odbc
import odbc_installer
import odbc

JET_DRIVER_NAME = "Microsoft Access Driver (*.mdb)"

import windll

def create (dsn, path, hwnd=0):
	# first, make sure the file doesn't already exist!
	if (os.path.isfile (path)):
		raise ValueError, "database file (%s) already exists!" % path
	else:
		# make sure path uses backslashes
		path = regsub.gsub ('/', '\\', path)
		# first, use CREATE_DB to create the database file
		result = odbc_installer.config_data_source (
			odbc_installer.ODBC_ADD_DSN,
			JET_DRIVER_NAME,
			'CREATE_DB=%s General\000\000' % path,
			hwnd
			)
		if result:
			# now create the ODBC DSN entry
			result = odbc_installer.config_data_source (
				odbc_installer.ODBC_ADD_DSN,
				JET_DRIVER_NAME,
				'DSN=%s\000DBQ=%s\000\000' % (dsn, path),
				hwnd
				)
		return result

def compact (dsn, path_src, path_dest=None, hwnd=0):
	if not os.path.isfile(path_src):
		raise ValueError, "database file (%s) does not exist!" % path_src
	else:
		if path_dest is None:
			path_dest = path_src
		path_src = regsub.gsub ('/', '\\', path_src)
		path_dest = regsub.gsub ('/', '\\', path_dest)
		result = odbc_installer.config_data_source (
			odbc_installer.ODBC_ADD_DSN,
			JET_DRIVER_NAME,
			'COMPACT_DB=%s %s General\000\000' % (path_src, path_dest),
			hwnd
			)
		return result

	
