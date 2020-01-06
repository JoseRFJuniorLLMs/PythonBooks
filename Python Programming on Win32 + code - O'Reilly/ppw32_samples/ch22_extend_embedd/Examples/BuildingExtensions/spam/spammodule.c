# include "Python.h"
/* pasted from Python extending/embedding manual*/

static PyObject *SpamError;

static PyObject *spam_system(self, args)
    PyObject *self;
    PyObject *args;
{
    char *command;
    int sts;
    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;    
	sts = system(command);
    return Py_BuildValue("i", sts);
}

static PyMethodDef SpamMethods[] = {
    {"system",  spam_system, METH_VARARGS},
    {NULL,      NULL}        /* Sentinel */
};


/* platform independent*/
#ifdef MS_WIN32
__declspec(dllexport)
#endif

void initspam3()
{
    PyObject *m, *d;

    m = Py_InitModule("spam3", SpamMethods);
    d = PyModule_GetDict(m);
    SpamError = PyErr_NewException("spam.error", NULL, NULL);
    PyDict_SetItemString(d, "error", SpamError);
}

