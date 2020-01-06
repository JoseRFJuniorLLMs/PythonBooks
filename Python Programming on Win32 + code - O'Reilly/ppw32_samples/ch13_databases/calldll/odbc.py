# -*- Mode: Python; tab-width: 4 -*-
#	Author: Sam Rushing <rushing@nightmare.com>
#
# ODBC interface via calldll, windll, etc...
#
# Notes:
#
# We ignore the 'real length of the return value' parameter for now.
# Overflows of string buffers are silently truncated.  Eventually I'd
# like to see a flexible way of handling all the various buffer types
# used by ODBC - most especially the ability to dynamically determine
# the types of fields in result sets.

import calldll
#from dyn_win32 import windll
import windll

cstring = windll.cstring

error = 'ODBC interface error'

# All odbc functions return 8-bit results (<sql.h>:SQLRETURN).
# Normally this isn't a problem, because with all other DLL's the
# extra bits are cleared.  But the combination of Win95 and odbc gets
# garbage in the top 16 bits.

# unsigned byte => signed byte
def frob_byte (byte):
	byte = byte & 0xff
	if byte > 127:
		return - (256 - byte)
	else:
		return byte

class odbc_function (windll.callable_function):
	def __call__ (self, *args):
		return frob_byte (apply (windll.callable_function.__call__, (self,) + args))

# The problem with this approach is that we lose windll.module()'s caching
# not a big deal, though.

class odbc_module (windll.cmodule):
	callable_function_class = odbc_function

odbc = odbc_module ('odbc32')

import string
import struct

# success values
# sql.h
SQL_INVALID_HANDLE		= -2
SQL_ERROR				= -1
SQL_SUCCESS				= 0
SQL_SUCCESS_WITH_INFO	= 1
SQL_STILL_EXECUTING		= 2
SQL_NEED_DATA			= 99
SQL_NO_DATA_FOUND		= 100

sql_errors = [SQL_ERROR, SQL_INVALID_HANDLE]

# sqlext.h
SQL_FETCH_NEXT		= 0x01
SQL_FETCH_FIRST		= 0x02
SQL_FETCH_LAST		= 0x04
SQL_FETCH_PRIOR		= 0x08
SQL_FETCH_ABSOLUTE	= 0x10
SQL_FETCH_RELATIVE	= 0x20
SQL_FETCH_RESUME	= 0x40
SQL_FETCH_BOOKMARK	= 0x80

# sql types
SQL_TYPE_NULL	= 0
SQL_CHAR		= 1
SQL_NUMERIC		= 2
SQL_DECIMAL		= 3
SQL_INTEGER		= 4
SQL_SMALLINT	= 5
SQL_FLOAT		= 6
SQL_REAL		= 7
SQL_DOUBLE		= 8
SQL_DATE		= 9
SQL_TIME		= 10
SQL_TIMESTAMP	= 11
SQL_VARCHAR		= 12

# SQL extended datatypes

SQL_LONGVARCHAR					= -1
SQL_BINARY						= -2
SQL_VARBINARY					= -3
SQL_LONGVARBINARY				= -4
SQL_BIGINT						= -5
SQL_TINYINT						= -6
SQL_BIT							= -7
SQL_INTERVAL_YEAR				= -80
SQL_INTERVAL_MONTH				= -81
SQL_INTERVAL_YEAR_TO_MONTH		= -82
SQL_INTERVAL_DAY				= -83
SQL_INTERVAL_HOUR				= -84
SQL_INTERVAL_MINUTE				= -85
SQL_INTERVAL_SECOND				= -86
SQL_INTERVAL_DAY_TO_HOUR		= -87
SQL_INTERVAL_DAY_TO_MINUTE		= -88
SQL_INTERVAL_DAY_TO_SECOND		= -89
SQL_INTERVAL_HOUR_TO_MINUTE		= -90
SQL_INTERVAL_HOUR_TO_SECOND		= -91
SQL_INTERVAL_MINUTE_TO_SECOND	= -92
SQL_UNICODE						= -95
SQL_UNICODE_VARCHAR				= -96
SQL_UNICODE_LONGVARCHAR			= -97
SQL_UNICODE_CHAR				= SQL_UNICODE
SQL_TYPE_DRIVER_START			= SQL_INTERVAL_YEAR
SQL_TYPE_DRIVER_END				= SQL_UNICODE_LONGVARCHAR
SQL_SIGNED_OFFSET				= -20
SQL_UNSIGNED_OFFSET				= -22

# Special length values (don't work yet)
SQL_NULL_DATA		= -1
SQL_DATA_AT_EXEC	= -2
SQL_NTS				= -3

# SQLGetInfo type types
STRING = 's'
INT16 = 'h'
INT32 = 'l'

# C datatype to SQL datatype mapping      SQL types 
SQL_C_CHAR    = SQL_CHAR             #  CHAR, VARCHAR, DECIMAL, NUMERIC 
SQL_C_LONG    = SQL_INTEGER          #  INTEGER                      
SQL_C_SHORT   = SQL_SMALLINT         #  SMALLINT                     
SQL_C_FLOAT   = SQL_REAL             #  REAL                         
SQL_C_DOUBLE  = SQL_DOUBLE           #  FLOAT, DOUBLE                
SQL_C_DEFAULT = 99
#
SQL_C_DATE       = SQL_DATE
SQL_C_TIME       = SQL_TIME
SQL_C_TIMESTAMP  = SQL_TIMESTAMP
SQL_C_BINARY     = SQL_BINARY
SQL_C_BIT        = SQL_BIT
SQL_C_TINYINT    = SQL_TINYINT
SQL_C_SLONG      = SQL_C_LONG+SQL_SIGNED_OFFSET    #  SIGNED INTEGER   
SQL_C_SSHORT     = SQL_C_SHORT+SQL_SIGNED_OFFSET   #  SIGNED SMALLINT  
SQL_C_STINYINT   = SQL_TINYINT+SQL_SIGNED_OFFSET   #  SIGNED TINYINT   
SQL_C_ULONG      = SQL_C_LONG+SQL_UNSIGNED_OFFSET  #  UNSIGNED INTEGER 
SQL_C_USHORT     = SQL_C_SHORT+SQL_UNSIGNED_OFFSET #  UNSIGNED SMALLINT
SQL_C_UTINYINT   = SQL_TINYINT+SQL_UNSIGNED_OFFSET #  UNSIGNED TINYINT 
SQL_C_BOOKMARK   = SQL_C_ULONG                     #  BOOKMARK         

# from "sql.h"
# Defines for SQLGetInfo
SQL_ACTIVE_CONNECTIONS				= 0,	INT16
SQL_ACTIVE_STATEMENTS				= 1,	INT16
SQL_DATA_SOURCE_NAME				= 2,	STRING
SQL_DRIVER_HDBC						= 3,	INT32
SQL_DRIVER_HENV						= 4,	INT32
SQL_DRIVER_HSTMT					= 5,	INT32
SQL_DRIVER_NAME						= 6,	STRING
SQL_DRIVER_VER						= 7,	STRING
SQL_FETCH_DIRECTION					= 8,	INT32
SQL_ODBC_API_CONFORMANCE			= 9,	INT16
SQL_ODBC_VER						= 10,	STRING
SQL_ROW_UPDATES						= 11,	STRING
SQL_ODBC_SAG_CLI_CONFORMANCE		= 12,	INT16
SQL_SERVER_NAME						= 13,	STRING
SQL_SEARCH_PATTERN_ESCAPE			= 14,	STRING
SQL_ODBC_SQL_CONFORMANCE			= 15,	INT16
SQL_DATABASE_NAME					= 16,	STRING
SQL_DBMS_NAME						= 17,	STRING
SQL_DBMS_VER						= 18,	STRING
SQL_ACCESSIBLE_TABLES				= 19,	STRING
SQL_ACCESSIBLE_PROCEDURES			= 20,	STRING
SQL_PROCEDURES						= 21,	STRING
SQL_CONCAT_NULL_BEHAVIOR			= 22,	INT16
SQL_CURSOR_COMMIT_BEHAVIOR			= 23,	INT16
SQL_CURSOR_ROLLBACK_BEHAVIOR		= 24,	INT16
SQL_DATA_SOURCE_READ_ONLY			= 25,	STRING
SQL_DEFAULT_TXN_ISOLATION			= 26,	INT32
SQL_EXPRESSIONS_IN_ORDERBY			= 27,	STRING
SQL_IDENTIFIER_CASE					= 28,	INT16
SQL_IDENTIFIER_QUOTE_CHAR			= 29,	STRING
SQL_MAX_COLUMN_NAME_LEN				= 30,	INT16
SQL_MAX_CURSOR_NAME_LEN				= 31,	INT16
SQL_MAX_OWNER_NAME_LEN				= 32,	INT16
SQL_MAX_PROCEDURE_NAME_LEN			= 33,	INT16
SQL_MAX_QUALIFIER_NAME_LEN			= 34,	INT16
SQL_MAX_TABLE_NAME_LEN				= 35,	INT16
SQL_MULT_RESULT_SETS				= 36,	STRING
SQL_MULTIPLE_ACTIVE_TXN				= 37,	STRING
SQL_OUTER_JOINS						= 38,	STRING
SQL_OWNER_TERM						= 39,	STRING
SQL_PROCEDURE_TERM					= 40,	STRING
SQL_QUALIFIER_NAME_SEPARATOR		= 41,	STRING
SQL_QUALIFIER_TERM					= 42,	STRING
SQL_SCROLL_CONCURRENCY				= 43,	INT32
SQL_SCROLL_OPTIONS					= 44,	INT32
SQL_TABLE_TERM						= 45,	STRING
SQL_TXN_CAPABLE						= 46,	INT16
SQL_USER_NAME						= 47,	STRING
SQL_CONVERT_FUNCTIONS				= 48,	INT32
SQL_NUMERIC_FUNCTIONS				= 49,	INT32
SQL_STRING_FUNCTIONS				= 50,	INT32
SQL_SYSTEM_FUNCTIONS				= 51,	INT32
SQL_TIMEDATE_FUNCTIONS				= 52,	INT32
SQL_CONVERT_BIGINT					= 53,	INT32
SQL_CONVERT_BINARY					= 54,	INT32
SQL_CONVERT_BIT						= 55,	INT32
SQL_CONVERT_CHAR					= 56,	INT32
SQL_CONVERT_DATE					= 57,	INT32
SQL_CONVERT_DECIMAL					= 58,	INT32
SQL_CONVERT_DOUBLE					= 59,	INT32
SQL_CONVERT_FLOAT					= 60,	INT32
SQL_CONVERT_INTEGER					= 61,	INT32
SQL_CONVERT_LONGVARCHAR				= 62,	INT32
SQL_CONVERT_NUMERIC					= 63,	INT32
SQL_CONVERT_REAL					= 64,	INT32
SQL_CONVERT_SMALLINT				= 65,	INT32
SQL_CONVERT_TIME					= 66,	INT32
SQL_CONVERT_TIMESTAMP				= 67,	INT32
SQL_CONVERT_TINYINT					= 68,	INT32
SQL_CONVERT_VARBINARY				= 69,	INT32
SQL_CONVERT_VARCHAR					= 70,	INT32
SQL_CONVERT_LONGVARBINARY			= 71,	INT32
SQL_TXN_ISOLATION_OPTION			= 72,	INT32
SQL_ODBC_SQL_OPT_IEF				= 73,	STRING
SQL_CORRELATION_NAME				= 74,	INT16
SQL_NON_NULLABLE_COLUMNS			= 75,	INT16
SQL_DRIVER_HLIB						= 76,	INT32
SQL_DRIVER_ODBC_VER					= 77,	STRING
SQL_LOCK_TYPES						= 78,	INT32
SQL_POS_OPERATIONS					= 79,	INT32
SQL_POSITIONED_STATEMENTS			= 80,	INT32
SQL_GETDATA_EXTENSIONS				= 81,	INT32
SQL_BOOKMARK_PERSISTENCE			= 82,	INT32
SQL_STATIC_SENSITIVITY				= 83,	INT32
SQL_FILE_USAGE						= 84,	INT16
SQL_NULL_COLLATION					= 85,	INT16
SQL_ALTER_TABLE						= 86,	INT32
SQL_COLUMN_ALIAS					= 87,	STRING
SQL_GROUP_BY						= 88,	INT16
SQL_KEYWORDS						= 89,	STRING
SQL_ORDER_BY_COLUMNS_IN_SELECT		= 90,	STRING
SQL_OWNER_USAGE						= 91,	INT32
SQL_QUALIFIER_USAGE					= 92,	INT32
SQL_QUOTED_IDENTIFIER_CASE			= 93,	INT32
SQL_SPECIAL_CHARACTERS				= 94,	STRING
SQL_SUBQUERIES						= 95,	INT32
SQL_UNION							= 96,	INT32
SQL_MAX_COLUMNS_IN_GROUP_BY			= 97,	INT16
SQL_MAX_COLUMNS_IN_INDEX			= 98,	INT16
SQL_MAX_COLUMNS_IN_ORDER_BY			= 99,	INT16
SQL_MAX_COLUMNS_IN_SELECT			= 100,	INT16
SQL_MAX_COLUMNS_IN_TABLE			= 101,	INT16
SQL_MAX_INDEX_SIZE					= 102,	INT32
SQL_MAX_ROW_SIZE_INCLUDES_LONG		= 103,	STRING
SQL_MAX_ROW_SIZE					= 104,	INT32
SQL_MAX_STATEMENT_LEN				= 105,	INT32
SQL_MAX_TABLES_IN_SELECT			= 106,	INT16
SQL_MAX_USER_NAME_LEN				= 107,	INT16
SQL_MAX_CHAR_LITERAL_LEN			= 108,	INT32
SQL_TIMEDATE_ADD_INTERVALS			= 109,	INT32
SQL_TIMEDATE_DIFF_INTERVALS			= 110,	INT32
SQL_NEED_LONG_DATA_LEN				= 111,	STRING
SQL_MAX_BINARY_LITERAL_LEN			= 112,	INT32
SQL_LIKE_ESCAPE_CLAUSE				= 113,	STRING
SQL_QUALIFIER_LOCATION				= 114,	INT16
#
# <Phew!>
#
#  Level 1 Prototypes                            

# <sqlext.h>
#  Options for SQLDriverConnect 
SQL_DRIVER_NOPROMPT             = 0
SQL_DRIVER_COMPLETE             = 1
SQL_DRIVER_PROMPT               = 2
SQL_DRIVER_COMPLETE_REQUIRED    = 3

# For SQLGetFunctions
SQL_API_ALL_FUNCTIONS			= 0

# Defines for SQLBindParameter and
# SQLProcedureColumns (returned in the result set)
SQL_PARAM_TYPE_UNKNOWN           = 0
SQL_PARAM_INPUT                  = 1
SQL_PARAM_INPUT_OUTPUT           = 2
SQL_RESULT_COL                   = 3
SQL_PARAM_OUTPUT                 = 4
SQL_RETURN_VALUE                 = 5

#  SQLFreeStmt defines 
SQL_CLOSE                       = 0
SQL_DROP                        = 1
SQL_UNBIND                      = 2
SQL_RESET_PARAMS                = 3


# 32-bit opaque handle
class opaque_handle:
	def __init__ (self):
		self.buffer = calldll.membuf (4) # c->w
		self.known = 0
	def ptr (self):
		self.known = 0
		return self.buffer.address()
	def value (self):
		if not self.known:
			self.known = 1
			(self.known_value,) = struct.unpack ('l', self.buffer.read())
		return self.known_value
	# automatic argument conversion to integer
	__int__ = value
	def __repr__ (self):
		return '<odbc %s handle 0x%x at 0x%x>' % (
			self.__class__.__name__,
			self.value(),
			id(self)
			)

class environment (opaque_handle):
	closed = 0

	def __init__ (self):
		opaque_handle.__init__ (self)
		if odbc.SQLAllocEnv (self.ptr()):
			raise error, 'SQLAllocEnv Failed'
		self.connections = []

	def data_sources (self):
		dsn = cstring ('', 255)
		dsnlen = calldll.membuf (4) # c->w
		desc = cstring ('', 511)
		desclen = calldll.membuf (4) # c->w
		result = []
		while 1:
			retval = odbc.SQLDataSources (
				self,
				SQL_FETCH_NEXT,
				dsn,
				len(dsn),
				dsnlen.address(),
				desc,
				len(desc),
				desclen.address(),
				)
			if retval == SQL_NO_DATA_FOUND:
				break
			elif retval == SQL_SUCCESS:
				result.append (dsn.trunc(), desc.trunc())
			else:
				raise error, 'SQLDataSources: %d' % retval
		return result

	def drivers (self):
		driver = cstring ('', 1023)
		driverlen = calldll.membuf (4) # c->w
		attr = cstring ('', 1023)
		attrlen = calldll.membuf (4) # c->w
		result = []
		while 1:
			retval = odbc.SQLDrivers (
				self,
				SQL_FETCH_NEXT,
				driver,
				len(driver),
				driverlen.address(),
				attr,
				len(attr),
				attrlen.address()
				)
			if retval == SQL_NO_DATA_FOUND:
				break
			elif retval == SQL_SUCCESS:
				result.append (driver.trunc(), attr.trunc())
			else:
				raise error, 'SQLDrivers: %d' % retval
		return result

	def connection (self):
		c = connection (self)
		self.connections.append (c)
		return c

	def __del__ (self):
		if not self.closed:
			self.close()

	def close (self):
		for c in self.connections:
			if c.connected:
				c.close()
		self.connections = []
		#print 'closing %s' % repr(self)
		retval = odbc.SQLFreeEnv (self)
		if retval:
			raise error, 'SQLFreeEnv: %d' % retval
		else:
			self.closed = 1

class connection (opaque_handle):
	def __init__ (self, environment):
		self.environment = environment
		opaque_handle.__init__ (self)
		self.connected = 0
		retval = odbc.SQLAllocConnect (environment, self.ptr())
		if retval:
			raise error, 'SQLAllocConnect Failed: %d' % retval

	def connect (self, dsn, uid='', auth=''):
		self.dsn	= cstring (dsn)
		self.uid	= cstring (uid)
		self.auth	= cstring (auth)
		retval = odbc.SQLConnect (
			self,							# connection handle
			self.dsn, self.dsn.strlen(),	# data source name
			self.uid, self.uid.strlen(),	# user identifier
			self.auth, self.auth.strlen(),	# authentication (password)
			)
		if retval in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
			self.connected = 1
		else:
			raise error, 'SQLConnect failed: %d' % retval

	# Extension level 2
	def browse_connect (self, connection_string, output_buffer_size=4096):
		out_buffer = windll.cstring ('', output_buffer_size)
		out_buffer_len = windll.membuf (2)
		connection_string = cstring (connection_string)
		result = odbc.SQLBrowseConnect (
			self,
			connection_string,
			connection_string.strlen(),
			out_buffer,
			output_buffer_size,
			out_buffer_len
			)
		if result not in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, SQL_NEED_DATA):
			sql_error (self.environment, self, 0)
		actual_length = struct.unpack ('h', out_buffer_len.read())[0]
		if actual_length == (output_buffer_size - 1):
			return self.browse_connect (connection_string, output_buffer_size * 2)
		else:
			self.connected = 1
			return (result, out_buffer.trunc())

	# Extension level 1
	def driver_connect (self,
						connection_string,
						driver_completion=SQL_DRIVER_NOPROMPT,
						output_buffer_size=1024,
						hwnd=0):
		out_buffer = windll.cstring ('', output_buffer_size)
		out_buffer_len = windll.membuf (2)
		connection_string = cstring (connection_string)
		result = odbc.SQLDriverConnect (
			self,
			hwnd,
			connection_string,
			SQL_NTS,
			out_buffer,
			output_buffer_size,
			out_buffer_len,
			driver_completion
			)
		if result:
			sql_error (self.environment, self, 0)
		actual_length = struct.unpack ('h', out_buffer_len.read())[0]
		if actual_length == (output_buffer_size - 1):
			return self.driver_connect (connection_string, output_buffer_size * 2, hwnd)
		else:
			return (result, out_buffer.trunc())

	def disconnect (self):
		if self.connected:
			#print 'disconnecting %s' % repr(self)
			result = odbc.SQLDisconnect (self)
			if result in sql_errors:
				sql_error (self.environment, self, 0)
				raise error, 'SQLDisconnect failed (%d)' % result
			self.connected = 0

	closed = 0

	def close (self):
		if not self.closed:
			self.disconnect()
			#print 'closing %s' % repr(self)
			result = odbc.SQLFreeConnect (self)
			if result in sql_errors:
				sql_error (self.environment, self, 0)
				raise error, 'SQLFreeConnect failed (%d)' % result
			else:
				self.closed = 1

	def __del__ (self):
		if not self.closed:
			self.close()

	def statement (self):
		return statement (self)

	def query (self, q, result_buffer=None, statement=None):
		if statement is None:
			st = self.statement()
		else:
			st = statement
		retval = st.exec_direct (q)
		if retval:
			sql_error (
				self.environment,
				self,
				st
				)
			return retval
		else:
			return st.get_result (result_buffer)

	# convenient  little dictionary interface
	def __getitem__ (self, key):
		return self.query (key)[1:]

	def get_info_low (self, type, buffer=None, size=511):
		if buffer is None:
			buffer = cstring ('\000'*size)
		retval_len = calldll.membuf (2) # c->w
		retval = odbc.SQLGetInfo (
			self,
			type,
			buffer,
			len(buffer),
			retval_len.address()
			)
		if retval:
			raise error, 'SQLGetInfo: %d' % retval
		return buffer

	def get_info_word (self, type):
		buffer = calldll.membuf (2) # c->w
		self.get_info_low (type, buffer)
		struct.unpack ('h', buffer.read())

	def get_info_long (self, type):
		buffer = calldll.membuf (4) # c->w
		self.get_info_low (type, buffer)
		struct.unpack ('l', buffer.read())

	def get_info_string (self, type, length=511):
		buffer = cstring ('\000'*length)
		self.get_info_low (type, buffer)
		return buffer.trunc()

	def get_info (self, (type, type_type)):
		if type_type == STRING:
			return self.get_info_string (type)
		elif type_type == INT16:
			return self.get_info_word (type)
		elif type_type == INT32:
			return self.get_info_long (type)
		else:
			raise error, 'Unknown type_type for SQLGetInfo'

	def get_functions (self, fun):
		if type(fun) == type(''):
			fun = string.lower (fun)
			if fun[:3] == 'sql':
				fun = fun[3:]
			if get_functions_table.has_key (fun):
				fun = get_functions_table[fun]
			else:
				raise ValueError, 'Unknown function name'
		if fun == SQL_API_ALL_FUNCTIONS:
			buffer = windll.membuf (2 * 100)
		else:
			buffer = windll.membuf (2)
		result = odbc.SQLGetFunctions (
			self,
			fun,
			buffer
			)
		if result:
			raise error, 'SQLGetFunctions Failed: %d' % result
		elif fun == SQL_API_ALL_FUNCTIONS:
			return struct.unpack ('h'*100, buffer.read())
		else:
			return struct.unpack ('h', buffer.read())[0]

class statement (opaque_handle):
	closed = 0

	def __init__ (self, connection):
		self.connection = connection
		opaque_handle.__init__ (self)
		retval = odbc.SQLAllocStmt (connection, self.ptr())
		if retval:
			raise error, 'SQLAllocStmt Failed: %d' % retval
			
	def close (self):
		#print 'closing %s' % repr(self)
		self.free()
		self.closed = 1
			
	def free (self, option=SQL_DROP):
		result = odbc.SQLFreeStmt (self, option)
		if result:
			sql_error (
				self.connection.environment,
				self.connection,
				self
				)
			raise error, 'SQLFreeStmt Failed: %d' % retval

	def __del__ (self):
		if not self.closed:
			self.close()

	# Access can't do this?
	def tables (self, qualifier=0, owner=0, name=0, type='TABLE'):

		def maybe_cstring (s):
			if s != 0:
				return cstring (s), len (s)
			else:
				return 0, 0
		
		q,ql = maybe_cstring (qualifier)
		o,ol = maybe_cstring (owner)
		n,nl = maybe_cstring (name)
		t,tl = maybe_cstring (type)
		retval = odbc.SQLTables (
			self,
			q,ql,
			o,ol,
			n,nl,
			t,tl
			)
		if retval:
			raise error, 'SQLTables: %d' % retval

	def columns (self, table_name, column_name=0, qualifier=0, owner=0):

		def maybe_cstring (s):
			if s != 0:
				return cstring (s), len (s)
			else:
				return 0, 0
		
		q,ql = maybe_cstring (qualifier)
		o,ol = maybe_cstring (owner)
		t,tl = maybe_cstring (table_name)
		c,cl = maybe_cstring (column_name)
		retval = odbc.SQLColumns (
			self,
			q,ql,
			o,ol,
			t,tl,
			c,cl
			)
		if retval:
			raise error, 'SQLColumns: %d' % retval

	def num_result_cols (self):
		cols = calldll.membuf (2) # c->w
		retval = odbc.SQLNumResultCols (
			self,
			cols.address()
			)
		return struct.unpack ('h', cols.read())[0]

	def describe_col (self, col):
		col_name = cstring ('', 255)
		col_name_len = calldll.membuf (2) # c->w
		sql_type = calldll.membuf (2) # c->w
		col_def = calldll.membuf (2) # c->w
		scale = calldll.membuf (2) # c->w
		nullable = calldll.membuf (2) # c->w
		retval = odbc.SQLDescribeCol (
			self,
			col,
			col_name, len(col_name), col_name_len.address(),
			sql_type.address(),
			col_def.address(),
			scale.address(),
			nullable.address()
			)
		return (col_name.trunc(),
				struct.unpack ('h',sql_type.read())[0],
				struct.unpack ('h',col_def.read())[0],
				struct.unpack ('h',scale.read())[0],
				struct.unpack ('h',nullable.read())[0]
				)

	def exec_direct (self, sql_str):
		sql_str = cstring (sql_str)
		retval = odbc.SQLExecDirect (self, sql_str, len(sql_str))
		if retval:
			sql_error (
				self.connection.environment,
				self.connection,
				self
				)
			raise error, 'SQLExecDirect: %d' % retval

	def fetch (self):
		return odbc.SQLFetch (self)

	buflen = calldll.membuf (4) # c->w
	# need to do fancy type handling here
	def get_data (self, col, type=SQL_CHAR, buffer=None):
		if buffer is None:
			buffer = cstring ('\000'*1023)
		retval = odbc.SQLGetData (
			self,
			col,
			type,
			buffer,
			len(buffer),
			self.buflen.address()
			)
		(real_len,) = struct.unpack ('l', self.buflen.read())
		if real_len == SQL_NULL_DATA:
			return retval, None
		return retval, buffer.trunc()

	# Thanks to Gordon McMillan (gmcm@hypernet.com) !
	def row_count (self):
		countbuff = calldll.membuf (4)
		rc = odbc.SQLRowCount (self, countbuff.address())
		if rc:
			sql_error (
				self.connection.environment,
				self.connection,
				self
				)
			raise error, 'SQLRowCount: %d' % rc
		(count,) = struct.unpack('l', countbuff.read())
		return count
	
	def get_result (self, buffer=None):
		num_cols = self.num_result_cols()
		result = [map (lambda x,s=self: s.describe_col (x+1), range(num_cols))]
		if buffer is None:
			buffer = cstring ('\000'*8192)
		while not self.fetch():
			row = []
			for i in range(num_cols):
				retval, data = self.get_data (i+1, SQL_CHAR, buffer)
				row.append (data)
			result.append (row)
		return result

	# apply a function to each row of the result
	def iterate_result (self, function, buffer=None):
		num_cols = self.num_result_cols()
		if buffer is None:
			buffer = cstring ('\000'*511)
		while not self.fetch():
			row =  []
			for i in range (num_cols):
				retval, data = self.get_data (i+1, SQL_CHAR, buffer)
				row.append (data)
			function(row)

	def prepare (self, sql_str):
		sql_str = cstring (sql_str)
		result = odbc.SQLPrepare (
			self,
			sql_str,
			len(sql_str)
			)
		if result:
			sql_error (
				self.connection.environment,
				self.connection,
				self
				)
			raise error, 'SQLPrepare: %d' % result

	def bind_parameter (self,
						# index of the parameter
						num,
						# buffer for input/output
						buffer,
						# choose [input, input/output, or output]
						param_type=SQL_PARAM_INPUT,
						c_type=SQL_C_DEFAULT,
						col_def=0,
						scale=0
						):
		result = odbc.SQLBindParameter (
			self,
			num,
			param_type,
			c_type,
			buffer.sql_type,
			buffer.col_def(),
			scale,
			buffer,
			len(buffer),
			buffer.length_capture_address
			)
		if result:
			sql_error (
				self.connection.environment,
				self.connection,
				self
				)
			raise error, 'SQLBindParameter: %d' % result

	def execute (self):
		result = odbc.SQLExecute (self)
		if result:
			sql_error (
				self.connection.environment,
				self.connection,
				self
				)
			raise error, 'SQLExecute: %d' % result

import types

# supported types:
# int
# float
# string

class parameter_buffer:
	int_len = len (struct.pack ('l', 0))
	float_len = len (struct.pack ('d', 0.0))
	def __init__ (self, param_type, length=None):
		self.length_capture = calldll.membuf(4) # c->w
		self.length_capture_address = self.length_capture.address()
		if param_type == types.IntType:
			self.mb = calldll.membuf (self.int_len) # c->w
			self.set_actual_length (self.int_len)
			self.set = self.set_integer
			self.get = self.get_integer
			self.sql_type = SQL_INTEGER
		elif param_type == types.FloatType:
			self.mb = calldll.membuf (self.float_len) # c->w
			self.set_actual_length (self.float_len)
			self.set = self.set_float
			self.get = self.get_float
			self.SQL_TYPE = SQL_DOUBLE
		elif param_type == types.StringType:
			self.mb = calldll.membuf (length) # c->w
			self.set = self.set_string
			self.get = self.get_string
			self.sql_type = SQL_CHAR
		else:
			raise ValueError, "Unsupported parameter type %s" % param_type
		self.param_type = param_type

	def grow (self, new_length):
		data = self.mb.read()
		self.mb = calldll.membuf (new_length) # c->w
		self.mb.write (data[:new_length])

	def __len__ (self):
		return self.mb.size()

	def __int__ (self):
		return self.mb.address()

	def col_def (self):
		return self.mb.size()

	def get_actual_length (self):
		return struct.unpack ('l', self.length_capture.read())[0]

	def set_actual_length (self, x):
		self.length_capture.write (struct.pack ('l', x))

	def set_integer (self, value):
		self.mb.write (struct.pack ('l', value))

	def set_float (self, value):
		self.mb.write (struct.pack ('d', value))

	def set_string (self, value):
		if (len(value) > self.mb.size()):
			print 'overflow!', len(value), value
			raise "Hell!"
			self.grow (len(value)+1)
		self.mb.write (value)
		self.set_actual_length (len(value))

	def get_integer (self):
		return struct.unpack ('l', self.mb.read())[0]

	def get_float (self):
		return struct.unpack ('d', self.mb.read())[0]

	def get_string (self, length=0):
		return self.mb.read()[:self.get_actual_length()]

def sql_error (env, dbc, stmt):
	error_msg = cstring ('', 511)
	sql_state = cstring ('', 63)
	native_error = calldll.membuf (2) # c->w
	errlen = calldll.membuf (2) # c->w
	result = odbc.SQLError (
		env,
		dbc,
		stmt,
		sql_state,
		native_error.address(),
		error_msg,
		len(error_msg),
		errlen.address()
		)
	print sql_state.trunc()
	print error_msg.trunc()
	print 'native error ',struct.unpack ('h',native_error.read())[0]

def test ():
	e = environment()
	print
	print 'data sources:'
	print '='*79
	for info in e.data_sources():
		print '%-40s %38s' % info
	print
	print 'drivers:'
	print '='*79
	for info in e.drivers():
		print '%-40s %38s' % info
	return e

if __name__ == '__main__':
	test()

# dumpbin /exports odbc32.dll reveals:
# ==================================================

# ConnectDlg
# PostError
# PostODBCError
# SQLAllocConnect
# SQLAllocEnv
# SQLAllocStmt
# SQLBindCol
# SQLBindParameter
# SQLBrowseConnect
# SQLCancel
# SQLColAttributes
# SQLColumnPrivileges
# SQLColumns
# SQLConnect
# SQLDataSources
# SQLDescribeCol
# SQLDescribeParam
# SQLDisconnect
# SQLDriverConnect
# SQLDrivers
# SQLError
# SQLExecDirect
# SQLExecute
# SQLExtendedFetch
# SQLFetch
# SQLForeignKeys
# SQLFreeConnect
# SQLFreeEnv
# SQLFreeStmt
# SQLGetConnectOption
# SQLGetCursorName
# SQLGetData
# SQLGetFunctions
# SQLGetInfo
# SQLGetStmtOption
# SQLGetTypeInfo
# SQLMoreResults
# SQLNativeSql
# SQLNumParams
# SQLNumResultCols
# SQLParamData
# SQLParamOptions
# SQLPrepare
# SQLPrimaryKeys
# SQLProcedureColumns
# SQLProcedures
# SQLPutData
# SQLRowCount
# SQLSetConnectOption
# SQLSetCursorName
# SQLSetParam
# SQLSetPos
# SQLSetScrollOptions
# SQLSetStmtOption
# SQLSpecialColumns
# SQLStatistics
# SQLTablePrivileges
# SQLTables
# SQLTransact

get_functions_table = {
	'allocconnect'		:1,    #  Core Functions           
	'allocenv'			:2,
	'allocstmt'			:3,
	'bindcol'			:4,
	'cancel'			:5,
	'colattributes'		:6,
	'connect'			:7,
	'describecol'		:8,
	'disconnect'		:9,
	'error'				:10,
	'execdirect'		:11,
	'execute'			:12,
	'fetch'				:13,
	'freeconnect'		:14,
	'freeenv'			:15,
	'freestmt'			:16,
	'getcursorname'		:17,
	'numresultcols'		:18,
	'prepare'			:19,
	'rowcount'			:20,
	'setcursorname'		:21,
	'setparam'			:22,
	'transact'			:23,
	'columns'			:40,    #  Level 1 Functions        
	'driverconnect'		:41,
	'getconnectoption'	:42,
	'getdata'			:43,
	'getfunctions'		:44,
	'getinfo'			:45,
	'getstmtoption'		:46,
	'gettypeinfo'		:47,
	'paramdata'			:48,
	'putdata'			:49,
	'setconnectoption'	:50,
	'setstmtoption'		:51,
	'specialcolumns'	:52,
	'statistics'		:53,
	'tables'			:54,
	'browseconnect'		:55,    #  Level 2 Functions        
	'columnprivileges'	:56,
	'datasources'		:57,
	'describeparam'		:58,
	'extendedfetch'		:59,
	'foreignkeys'		:60,
	'moreresults'		:61,
	'nativesql'			:62,
	'numparams'			:63,
	'paramoptions'		:64,
	'primarykeys'		:65,
	'procedurecolumns'	:66,
	'procedures'		:67,
	'setpos'			:68,
	'setscrolloptions'	:69,
	'tableprivileges'	:70,
	'drivers'			:71,
	'bindparameter'		:72,
	}
