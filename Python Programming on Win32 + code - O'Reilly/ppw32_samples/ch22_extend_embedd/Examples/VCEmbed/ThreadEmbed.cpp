/* ThreadEmbed.cpp

A sample showing how to embed Python in a multi-threaded
application (with copious cut-and-pasting from the standard
Python emnbedding demo).

The threading related concepts use the Windows
specific helper CEnterLeavePython, defined in PyWinTypes.dll

It needs to be used in conjunction with ThreadEmbed.py

Some error checking ommited, but there are comments where
it should be!
*/

int main(char *(argv, int argc)
{
    // Pass argv[0] to the Python interpreter
    Py_SetProgramName(argv[0]);

    // Initialize the Python interpreter.  Required.
    Py_Initialize();

	// Initialize our static, embedded app specific module
    initmyapp();
	
    // Import the Python module that does our work
    extModule = PyImport_ImportModule("ThreadEmbed")
    if (extModule == NULL) {
        cout << "Could not locate the Python extension module";
        return 1;
    // Get the function we wish to call
    startFunction = PyObject_GetAttr(extModule, "StartFunction");

    // Free the reference to the module object we no longer need
    Py_DECREF(extModule);

    // Check we did indeed get an object back, and it is callable
    if (startFunction==NULL || !PyCallable_Check(startFunction)) {
        Py_XDECREF(startFunction);
        cout << "There is no StartFunction, or it is not callable!";
        return 1
    }
    // Make the arguments for the call
    // We hard-code the arguments.
    args = Py_BuildValue("si", "Hello", 5);
    // We should check args!=NULL, but we assume life is good!

    // Make the call
    result = PyObject_Call(startFunction, args);
    // Free our reference to the args and function object.
    Py_DECREF(args);
    if (result == NULL) {
        cout << "Calling the start function failed!";
        return 1;
    }
    // We should check the result is indeed a PyInt object.
    cout << "The function returned " << PyInt_AsLong(result);

    // Free our reference to the result object.
    Py_DECREF(result);

    // Pretend we are off doing real work, but really we are sleeping!
    Sleep(5000); // 3 seconds.

    // We should now call another "StopFunction", so that
    // our threads created in Python have a chance to stop.
    // However, we will just exit here, aborting our threads

    // We should also call Py_Terminate, but wont as we arent
    // stopping these other threads.
}


