#include "Python.h"

static PyObject *
stats_mavm(self, args)
     PyObject *self, *args;
{
   float         value[4], total;
   float         minimum =  1E32;
   float         maximum = -1E32;
   int            i;

   if (!PyArg_ParseTuple (args, "ffff", &value[0], &value[1], 
			  &value[2], &value[3]))
      return NULL;

   for (i=0; i<4; i++)
   {
      if (value[i] < minimum)
          minimum = value[i];
      if (value[i] > maximum)
          maximum = value[i];
      total = total + value[i];
   }

   return Py_BuildValue("(fff)", minimum, total/4, maximum) ;
}

static PyMethodDef statistics_methods[] = {
        {"mavm",     stats_mavm,   1,  "Min, Avg, Max"},
        {NULL, NULL}
};

DL_EXPORT(void)
initstatistics()
{
	Py_InitModule("statistics", statistics_methods);
}

