# -*- Mode: Python; tab-width: 4 -*-

import struct
import string

#from dyn_win32 import windll
import windll

INSTALLER_NAME = 'odbccp32'

cstring = windll.cstring
#install = windll.module ('odbccp32')
user32  = windll.module ('user32')

import os

INSTALL = None

# Many applications do not need to have the installer loaded into
# memory for long.  We provide the ability to '[un]load-on-demand'
#
# After you're finished with the module, call 'unload_installer()'.
# [be aware that this all works through reference counting....]

def get_installer (name=INSTALLER_NAME):
	global INSTALL
	if INSTALL is None:
		print 'loading installer...'
		INSTALL = windll.cmodule (name)
	return INSTALL

def unload_installer (name=INSTALLER_NAME):
	# if there are no other references to the module, it will
	# unload...
	global INSTALL
	INSTALL = None

def reload_installer (name=INSTALLER_NAME):
	global INSTALL
	INSTALL = get_installer()

# ===========================================================================
# from <odbcinst.h>
# ===========================================================================

# SQLConfigDataSource request flags
ODBC_ADD_DSN		= 1		# Add data source
ODBC_CONFIG_DSN		= 2		# Configure (edit) data source
ODBC_REMOVE_DSN		= 3		# Remove data source

ODBC_ADD_SYS_DSN	= 4		# add a system DSN
ODBC_CONFIG_SYS_DSN	= 5		# Configure a system DSN
ODBC_REMOVE_SYS_DSN	= 6		# remove a system DSN

# install request flags
ODBC_INSTALL_INQUIRY	= 1		
ODBC_INSTALL_COMPLETE	= 2

# config driver flags
ODBC_INSTALL_DRIVER		= 1
ODBC_REMOVE_DRIVER		= 2
ODBC_CONFIG_DRIVER_MAX	= 100

# ===========================================================================

def get_installed_drivers (buffer_length=4096):
	buf = windll.membuf (buffer_length)
	buf_out = windll.membuf (2)
	result = get_installer().SQLGetInstalledDrivers (buf, buffer_length, buf_out)
	if not result:
		raise SystemError, "SQLGetInstalledDrivers() failed"
	else:
		actual_length = struct.unpack ('h', buf_out.read())[0]
		if actual_length == (buffer_length - 1):
			return get_installed_drivers (buffer_length * 2)
		else:
			return string.split (buf.read()[:actual_length-1], '\000')

def config_data_source (request, driver, attributes, hwnd=0):
	driver = cstring (driver)
	attributes = cstring (attributes, remember=1)
	result = get_installer().SQLConfigDataSource (
		hwnd,
		request,
		driver,
		attributes
		)
	if not result:
		raise SystemError, "SQLConfigDataSource() failed"
	return result

def config_dsn (request, driver, attributes, hwnd=user32.GetDesktopWindow()):
	driver = cstring (driver)
	attributes = cstring (attributes)
	return get_installer().ConfigDSN (
		hwnd,
		request,
		driver,
		attributes
		)

def create_data_source (name, hwnd=user32.GetDesktopWindow()):
	name = cstring (name)
	return get_installer().SQLCreateDataSource (hwnd, name)

def install_odbc (inf_path, src_path, drivers, hwnd=0):
	global install
	installer = windll.cmodule (os.path.join (src_path, 'odbccp32'))
	[inf_path, src_path, drivers] = map (cstring, [inf_path, src_path, drivers])
	result = installer.SQLInstallODBC (
		hwnd,
		inf_path,
		src_path,
		drivers
		)
	installer.unload()
	if result:
		# this probably doesn't do what I want it to do, since
		# SQLInstallODBC() seems to require the files are in the
		# current directory, this will simply reload the copy in '.'
		# no big deal?  [unless it's on a floppy?]
		install = windll.module ('odbccp32')
	return result

# After considerable digging through documentation, I have found the
# magical incantations necessary for creating, compacting, and
# repairing Jet databases through ODBC.  There are several locations
# in the documentation where we are told that this can't be done (See
# "FAQ: Programmatically Configuring an ODBC Data Source").   However,
# the article "INF: Accessing CREATE_DB, REPAIR_DB, and COMPACT_DB"
# (Q126606) says otherwise...
# Here's a snippet of code with some sample ConfigDataSource 'attribute'
# arguments: (must be called in sequence)
#
#     UCHAR szDriver[] = "Microsoft Access Driver (*.mdb)";
#     UCHAR *szAttributes2[] =
#     // Create the original .mdb file.
#     {"CREATE_DB=c:\\odbcsdk\\smpldata\\access\\general.mdb General\0\0",
# 
#     // Issue a REPAIR_DB on the created file.
#     "REPAIR_DB=c:\\odbcsdk\\smpldata\\access\\general.mdb\0\0",
# 
#     // Compact the file into a new location.
#     "COMPACT_DB=c:\\odbcsdk\\smpldata\\access\\general.mdb "
#       "c:\\odbcsdk\\smpldata\\access\\general2.mdb General\0\0",
# 
#     // Compact the file onto itself.
#     "COMPACT_DB=c:\\odbcsdk\\smpldata\\access\\general.mdb "
#       "c:\\odbcsdk\\smpldata\\access\\general.mdb General\0\0",
# 
#     // Create a datasource for the first .mdb file created.
#     "DSN=albacc\0FIL=MS Access\0JetIniPath=odbcddp.ini\0"
#     "DBQ=c:\\odbcsdk\\smpldata\\access\\general.mdb\0"
#     "DefaultDir=c:\\odbcsdk\\smpldata\\access\0\0"};
#
#
# And here's a bit in python:
# Example: Create and initialize a Jet database through ODBC.  Note
# that the keywords used are database-specific. (i.e., a completely
# different attribute string is necessary to create an SQL Server
# database).
#
# >>> import odbc
# >>> import odbc_installer
# >>> i = odbc_installer
# >>> i.config_data_source (i.ODBC_ADD_DSN, 'Microsoft Access Driver (*.mdb)', 'CREATE_DB=e:\\temp\\zc.mdb General;')
# >>> i.config_data_source (i.ODBC_ADD_DSN, 'Microsoft Access Driver (*.mdb)', 'DSN=zc;DBQ=e:\\temp\\zc.mdb;')
# >>> e = odbc.environment()
# >>> c = e.connection()
# >>> c.connect ('zc')
# >>> c.query ('CREATE TABLE fnord (name char(10), num integer);')
# [[]]
# >>> c.query ("insert into fnord (name, num) values ('Sam', 27);")
# [[]]
# >>> c.query ('select * from fnord')
# [[('name', 1, 10, 0, 1), ('num', 4, 10, 0, 1)], ['Sam       ', '27']]
# >>> c.close()
