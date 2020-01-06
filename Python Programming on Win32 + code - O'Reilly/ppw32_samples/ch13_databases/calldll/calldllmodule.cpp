// -*- Mode: C++; tab-width: 4 -*-
//	Author: Sam Rushing <rushing@nightmare.com>

#include <windows.h>

/* Define this if you want to keep track of <membuf> allocation */
#undef DEBUG_MEMBUF

#include "Python.h"

static PyObject *calldll_module_error;

/* It'd be nice to use __declspec (thread), but it doesn't work with
 * DLL's */

DWORD thread_state_tls_index;

#define FETCH_THREAD_STATE() ( (PyThreadState *) TlsGetValue (thread_state_tls_index) )
#define STORE_THREAD_STATE(value) ( TlsSetValue (thread_state_tls_index, ((LPVOID)value)) )

/* This is used by trampolines created by the gencb module, in place
 * of a normal call to PyEval_CallObject */

PyObject *
thread_safe_call_object (PyObject * fun, PyObject * args)
{
  PyObject * result;

  PyEval_RestoreThread (FETCH_THREAD_STATE());

  result = PyEval_CallObject (fun, args);

  STORE_THREAD_STATE (PyEval_SaveThread());

  return result;
}

//
// adapated from MIT Scheme, 7.3, microcode/ntgui.c.
//

static long
call_ff_really (long function_address,
				char * arg_format_string,
				PyObject * arg_tuple,
				long * result_addr)
{
  {
	/*	use a struct for locals that live across the foreign function call
		so that their position in the stack is the right end of the stack
		frame with respect to the stacked C arguments */
	struct {
	  long c_args[30];
	  long old_esp;
	} local;
	
	long result;

	/*	We save the stack pointer and restore it because the called function
		may pop the arguments (pascal/__stdcall) or expect us to (__cdecl). */

	/*	The stack pointer is saved in a static variable so that we can find
		it if the compiler does SP-relative addressing with a broken SP */
	
	/*	The implication is that things will break if this gets overwritten.
		This will happen if the foreign function directly or indirectly 
		allows a Scheme interrupt to be processed (eg by calling as scheme
		function with interrupts enabled and that function gets rescheduled
		in the threads package. */
	
	static long saved_esp;
	
	{
	  long *arg_sp = &local.c_args[10];
	  long	funadd = function_address;

	  if (!PyArg_ParseTuple (arg_tuple,
							 arg_format_string,
							 &local.c_args[10],
							 &local.c_args[11],
							 &local.c_args[12],
							 &local.c_args[13],
							 &local.c_args[14],
							 &local.c_args[15],
							 &local.c_args[16],
							 &local.c_args[17],
							 &local.c_args[18],
							 &local.c_args[19],
							 &local.c_args[20],
							 &local.c_args[21],
							 &local.c_args[22],
							 &local.c_args[23],
							 &local.c_args[24],
							 &local.c_args[25],
							 &local.c_args[26],
							 &local.c_args[27],
							 &local.c_args[28],
							 &local.c_args[29])) {
		return 0;
	  }

	  STORE_THREAD_STATE (PyEval_SaveThread());

	  arg_sp = &local.c_args[10];
	  local.old_esp = saved_esp;
	  __asm
		{
		  // Important: The order of these instructions guards against
		  // stack pointer relative addressing.
		  mov	eax, dword ptr [funadd]
		  mov	dword ptr [saved_esp], esp
		  mov	esp, dword ptr [arg_sp]
		  call	eax
		  mov	esp, dword ptr [saved_esp]
		  mov	dword ptr [result], eax
		}
		saved_esp = local.old_esp;

		PyEval_RestoreThread (FETCH_THREAD_STATE());
		
		*result_addr = result;
		return 1;
	}
  }
}


static
PyObject *
call_foreign_function (PyObject * self, PyObject * args)
{
  long function_address;
  char * arg_format_string;
  char * result_format_string;
  PyObject * arg_tuple;
  long result;

  if (!PyArg_ParseTuple (args, "lssO",
						 &function_address,
						 &arg_format_string,
						 &result_format_string,
						 &arg_tuple)) {
	return NULL;
  } else {
	long status;

	status = call_ff_really (function_address, arg_format_string, arg_tuple, &result);

	if (!status) {
	  return NULL;
	} else {
	  return Py_BuildValue (result_format_string, result);
	}
  }
}

static PyObject *
py_load_library (PyObject * self, PyObject * args)
{
  LPCTSTR name;
  if (!PyArg_ParseTuple (args, "s", &name)) {
	return NULL;
  } else {
	return Py_BuildValue ("l", ::LoadLibrary (name));
  }
}

static PyObject *
py_get_module_handle (PyObject * self, PyObject * args)
{
  LPCTSTR name;
  if (!PyArg_ParseTuple (args, "s", &name)) {
	return NULL;
  } else {
	return Py_BuildValue ("l", ::GetModuleHandle (name));
  }
}

static PyObject *
py_free_library (PyObject * self, PyObject * args)
{
  HMODULE dll_handle;
  if (!PyArg_ParseTuple (args, "l", &dll_handle)) {
	return NULL;
  } else {
	return Py_BuildValue ("i", (int) ::FreeLibrary (dll_handle));
  }
}

static PyObject *
py_get_proc_address (PyObject * self, PyObject * args)
{
  HMODULE dll_handle;
  LPCSTR proc_name;
  
  if (!PyArg_ParseTuple (args, "ls", &dll_handle, &proc_name)) {
	return NULL;
  } else {
	return Py_BuildValue ("l", (long) ::GetProcAddress (dll_handle, proc_name));
  }
}

static PyObject *
py_read_long (PyObject * self, PyObject * args)
{
  void * address;

  if (!PyArg_ParseTuple (args, "l", &address)) {
	return NULL;
  } else {
	return Py_BuildValue ("l", *((long *)address));
  }
}

static PyObject *
py_read_byte (PyObject * self, PyObject * args)
{
  void * address;

  if (!PyArg_ParseTuple (args, "l", &address)) {
	return NULL;
  } else {
	return Py_BuildValue ("b", *((char *)address));
  }
}

static PyObject *
py_read_string (PyObject * self, PyObject * args)
{
  void * address;
  int length = 0;

  if (!PyArg_ParseTuple (args, "l|i", &address, &length)) {
	return NULL;
  } else if (length == 0) {
	return Py_BuildValue ("s", (char *)address);
  } else {
	return Py_BuildValue ("s#", (char *)address, length);
  }
}

// ===========================================================================
// memory buffer objects
// ===========================================================================

typedef struct {
	PyObject_HEAD
	void *	buffer;
	size_t	size;
    int allocated;
} membuf_object;

#ifdef DEBUG_MEMBUF
unsigned int membuf_allocated;
unsigned int membuf_freed;
#include <stdio.h>
#endif

static void
membuf_object_dealloc(membuf_object * m_obj)
{
  if (m_obj->allocated) {
#ifdef DEBUG_MEMBUF
	membuf_freed += m_obj->size;
#endif  
	free (m_obj->buffer);
  }
  PyMem_DEL(m_obj);
}

static PyObject *
membuf_read_method (membuf_object * self,
					PyObject * args)
{
  unsigned int offset = 0;
  unsigned int size = 0;
  
  if (!PyArg_ParseTuple (args, "|ii", &offset, &size)) {
    return(NULL);
  }

  if ((offset + size) > self->size) {
	PyErr_SetString (PyExc_ValueError, "offset+size is larger than buffer");
	return NULL;
  } else {
	return Py_BuildValue ("s#", ((char *)(self->buffer)) + offset, size ? size : self->size);
  }
}

static PyObject *
membuf_write_method (membuf_object * self,
					 PyObject * args)
{
  int offset=0;
  unsigned int length=0;
  int string_length;
  char * data;

  if (!PyArg_ParseTuple (args, "s#|ii", &data, &string_length, &offset, &length)) {
    return(NULL);
  } else if (length == 0) {
	length = string_length;
  }

  if (length > self->size) {
	PyErr_SetString (PyExc_ValueError, "input string size is larger than buffer");
	return NULL;
  } else {
	memcpy (((char *)(self->buffer))+offset, data, length);
	Py_INCREF (Py_None);
	return (Py_None);
  }
}

static PyObject *
membuf_size_method (membuf_object * self,
					PyObject * args)
{
  if (!PyArg_ParseTuple (args, "")) {
	return NULL;
  } else {
	return Py_BuildValue ("i", self->size);
  }
}

static PyObject *
membuf_address_method (membuf_object * self,
					   PyObject * args)
{
  if (!PyArg_ParseTuple (args, "")) {
	return NULL;
  } else {
	return Py_BuildValue ("l", (long)(self->buffer));
  }
}

static struct PyMethodDef membuf_object_methods[] = {
  {"read",		(PyCFunction)	membuf_read_method,		1},
  {"write",		(PyCFunction)	membuf_write_method,	1},
  {"size",		(PyCFunction)	membuf_size_method,		1},
  {"address",	(PyCFunction)	membuf_address_method,	1},
  {"__int__",	(PyCFunction)	membuf_address_method,	1},
  {NULL,		NULL}		/* sentinel */
};

static PyObject *
membuf_object_getattr(membuf_object * self, char * name)
{
  return Py_FindMethod (membuf_object_methods, (PyObject *)self, name);
}

static PyTypeObject membuf_object_type = {
	PyObject_HEAD_INIT(&PyType_Type)
	0,							// ob_size
	"membuf",					// tp_name
	sizeof(membuf_object), 		// tp_size
	0,							// tp_itemsize
	// methods
	(destructor) membuf_object_dealloc,// tp_dealloc
	0,							// tp_print
	(getattrfunc) membuf_object_getattr, // tp_getattr
	0,							// tp_setattr
	0,							// tp_compare
	0,							// tp_repr
	0,							// tp_as_number
};

static PyObject *
new_membuf_object (PyObject * self, PyObject * args)
{
  membuf_object * m_obj;
  void * address = NULL;
  int size;

  if (!PyArg_ParseTuple (args, "i|l", &size, &address)) {
	return NULL;
  } else {
	m_obj = PyObject_NEW (membuf_object, &membuf_object_type);

	if (!m_obj) {
	  PyErr_SetString (PyExc_MemoryError, "couldn't allocate memory for buffer object");
	  return NULL;
	}
	
	if (address) {
	  /* we want a pointer into existing memory */
	  m_obj->allocated = 0;
	  m_obj->buffer = address;
	  m_obj->size = size;
	  return (PyObject *) m_obj;
	} else {
	  /* we want a new memory buffer */
	  void * buffer = (void *) malloc (size);

	  if (!buffer) {
		PyErr_SetString (PyExc_MemoryError, "couldn't allocate memory for buffer");
		PyMem_DEL (m_obj);
		return NULL;
	  } else {
#ifdef DEBUG_MEMBUF
		membuf_allocated += size;
#endif
		m_obj->allocated = 1;
		m_obj->size = size;
		m_obj->buffer = buffer;
		return (PyObject *) m_obj;
	  }
	}
  }
}

#ifdef DEBUG_MEMBUF
static PyObject *
membuf_allocation (PyObject * self, PyObject * args)
{
  if (!PyArg_ParseTuple (args, "")) {
	return NULL;
  } else {
	return Py_BuildValue ("ll", membuf_allocated, membuf_freed);
  }
}
#endif

// ===========================================================================
//
// ===========================================================================

/* List of functions exported by this module */
static struct PyMethodDef calldll_functions[] = {
  {"call_foreign_function",	(PyCFunction) call_foreign_function,1},
  {"load_library",			(PyCFunction) py_load_library,		1},
  {"free_library",			(PyCFunction) py_free_library,		1},
  {"get_module_handle",		(PyCFunction) py_get_module_handle, 1},  
  {"get_proc_address",		(PyCFunction) py_get_proc_address,	1},
  {"read_long",				(PyCFunction) py_read_long,			1},
  {"read_byte",				(PyCFunction) py_read_byte,			1},
  {"read_string",			(PyCFunction) py_read_string,		1},
  {"membuf",				(PyCFunction) new_membuf_object,	1},
#ifdef DEBUG_MEMBUF
  {"membuf_allocation",		(PyCFunction) membuf_allocation,	1},
#endif
  {NULL,			NULL}		 /* Sentinel */
};


void
initcalldll(void)
{
	PyObject *dict, *module;
	module = Py_InitModule ("calldll", calldll_functions);
	dict = PyModule_GetDict (module);
	calldll_module_error = PyString_FromString ("calldll error");
	PyDict_SetItemString (dict, "error", calldll_module_error);

	/* initialize our thread local storage index */
	thread_state_tls_index = TlsAlloc();

	/* This is not actually needed, we could just use
	   calldll.get_proc_address to get them! */

	PyDict_SetItemString (
	  dict,
	  "addrs",
	  Py_BuildValue (
		"(lll)",
		&Py_BuildValue,
		&PyInt_AsLong,
		/* &PyEval_CallObject */ /* OR */ &thread_safe_call_object
		)
	);
}
