
I've thrown together a simple foreign function interface, using some
code lifted from MIT Scheme.

You can use it to call functions in arbitrary DLL's.  It should work
for both __stdcall and __cdecl functions.

[Note: You can't use this with 16-bit DLL's.  For that you need to
 use the thunking library, which I thankfully know nothing about.]

[Note: calldll.call_foreign_function does not yet support
 returning 64-bit quantities (like C doubles).  They are returned
 using a different convention]

===========================================================================
There are a few very standard windows functions represented in this
module, which allow you to get at DLL's and function pointers:

>>> calldll.load_library (library_name)

will attempt to load a dll (map it into your address space), and
return a module handle or zero.

>>> calldll.get_module_handle (library_name)

will return the handle of a library if it is already loaded, or zero.

>>> calldll.get_proc_address (module_handle, procedure_name)

will return the address of a procedure if it's exported by the module,
or zero.

Many standard windows functions have two entry points, with either an
'A' or a 'W' appended to the name.  These are the 'ascii' and 'wide
char' variants of those functions that deal with strings.

If you have the 'dumpbin' utility (comes with visual c++), you can see
what symbols are exported by a 32-bit dll like this:

d:\winnt\system32> dumpbin /exports user32.dll

To call a function, once you have its address:

calldll.call_foreign_function (
  function_address,
  in_args_format_string,
  result_format_string,
  argument_tuple
  )

where <in_args_format_string> is a standard PyArg_ParseTuple string,
and <result_format_string> is a single-char string which is used to
build a python return value from the result of the function call.

===========================================================================
calldll has a simple memory buffer object, which can be used to pass
buffers to dll calls.  You can read and write strings from a <membuf>
object.  There are also a few functions for reading from arbitrary
memory addresses.

# create a 64-byte buffer
>>> my_struct = calldll.membuf (64)
# get the address of the start of the buffer:
>>> my_struct.address()

===========================================================================
There are a few utility modules which make <calldll> a little
easier to use.

[Note, the previous 'windll.WIN' interface has been removed. I've
 found that I prefer using the windll.module object directly]

The following sequence shows how you might use 'windll.py' to call
a function in a DLL:

>>> import windll
>>> kernel32 = windll.module ('kernel32')
>>> kernel32.Beep (1000, 50)

windll automatically gets the procedure's address, and caches
everything, so the next time you use 'kernel32.Beep' it'll just be a
dictionary lookup.

Your win32 documentation should tell you which library a particular
win32 function is in... If you're using Visual C++, click on the
'Quick Info' button in the InfoViewer Topic window.

===========================================================================

I've now added a callback-generating facility.  This removes the final
barrier to writing full-blown win32 applications completely in python
- many win32 functions require the addresses of a callback function
in order to work.  A window procedure would be the most obvious
example of this.  But you can't pass the address of a Python function
object, can you! 8^)

The module 'gencb.py' will generate a snippet of x86 assembly code
that will act as a wrapper for a python function object.  The code
translates the given arguments into a tuple (using Py_BuildValue) and
then calls PyEval_CallObject().

See 'cbdemo.py' for a demonstration.  There are also a few other
modules (in various stages of completeness) that might eventually form
the core of a Python 'Class Library' for programming Windows.

===========================================================================

An alternate version of the 'npstruct' module is available, implemented
as a C extension module.  If your bit-twiddling needs speeding up, look
for that package here:

  http://www.nightmare.com/software.html

===========================================================================
(July 24, 1998)

With the assistance of Christian Tismer, Gordon McMillan, and Mark Hammond
I have now (I believe) made calldll and gencb thread-safe.

Multiple GUI threads are still not working; if you try to create other
windows in other threads it will _start_ to work, and then crash.  If
someone can figure this out please let me know!

This isn't much of a real restriction, though, since the GDI itself is
not thread safe, it's quite a snake's nest (ahem) to make it work.  I
believe that MFC makes a similar restriction on the use of threads.

'Worker Threads' seem to work just fine.

-Sam
rushing@nightmare.com
