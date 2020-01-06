#include "Python.h"

static PyObject *
stats_mavm(self, args)
     PyObject *self, *args;
{
   float          total;
   float          minimum     =  1E32;
   float          maximum     = -1E32;
   int            i, len;
   char           message[80];
   PyObject      *idataList;
   PyFloatObject *f           = NULL;
   double         df;

   if (!PyArg_ParseTuple (args, "O", &idataList[0]))
      return NULL;

   /* check first to make sure we've got a list */
   if (!PyList_Check(idataList))
   {
      PyErr_SetString(PyExc_TypeError,
	 "input argument must be a list");
      return NULL;
   }

   len = PyList_Size(idataList);

   for (i=0; i<len; i++)
   {
      f = PyList_GetItem(idataList, i);
      df = PyFloat_AsDouble(f);
      if (df < minimum)
         minimum = value[i];
      if (df > maximum)
         maximum = value[i];
      total = total + df;
   }

   return Py_BuildValue("(fff)", minimum, total/len, maximum) ;
}

static PyMethodDef statistics_methods[] = {
        {"mavm",     stats_mavm,   1,  "Min, Avg, Max"},
        {NULL, NULL}
};

void
initstatistics()
{
	Py_InitModule("statistics", statistics_methods);
}

