#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <time.h>
#include <stdlib.h>

#include "Python.h"

PyObject *rDict = NULL;  /* Keep these global */
PyObject *instanceDict; 

/* 
**   Initializes the dictionary
**   Returns TRUE if successful, FALSE otherwise
*/

int 
initDictionary(char *name)
{
  PyObject *importModule;

  int retval = 0;

  /*   ***************** Initialize interpreter *******************   */

  Py_Initialize();

  /* Import a borrowed reference to the dict Module  */
  if ((importModule = PyImport_ImportModule("dict")))
  {
    /* Get a borrowed reference to the dictionary instance */                
    if ((instanceDict = PyObject_CallMethod(importModule, "Dictionary", 
					    "s", name)))
    {
      /* Store a global reference to the dictionary */
      rDict = PyObject_GetAttrString(instanceDict, "dictionary");
      if (rDict != NULL)
	retval = 1;
    }
    else
    {
      printf("Failed to initialize dictionary\n");
    }
  }
  else
  {
    printf("import of dict failed\n");
  }
  return (retval);
}

/* 
**   Finalizes the dictionary
**   Returns TRUE 
*/

int 
exitDictionary(void)
{

  /*   ***************** Finalize interpreter *******************   */
  Py_Finalize();

  return (1);
}

/*
**   Returns the information in buffer (which caller supplies)
*/

void
getInfo(char *who, char *buffer)
{
  PyObject *reference;

  int      birthYear;
  int      deathYear;
  char    *birthPlace;
  char    *degree;

  *buffer = '\0';

  if (rDict)
  {
    if ((reference = PyDict_GetItemString( rDict, who )))
    {
      if (PyTuple_Check(reference))
      {
        if (PyArg_ParseTuple(reference, "iiss", 
		     &birthYear, &deathYear, &birthPlace, &degree))
        {
	  sprintf(buffer, "%s was born at %s in %d. His degree is in %s\n",
		  who, birthPlace, birthYear, degree);
	  if (deathYear > 0)
	    sprintf((buffer+strlen(buffer)), "He died in %d\n", deathYear);
	}
      }
    }
    else
      strcpy(buffer, "No information\n");
  }
  return;
}


main()
{
  static char  buf[256];

  initDictionary("Not Used");

  getInfo("Michael Palin", buf);
  printf(buf);

  getInfo("Spiny Norman", buf);
  printf(buf);

  getInfo("Graham Chapman", buf);
  printf(buf);

  exitDictionary();
}
