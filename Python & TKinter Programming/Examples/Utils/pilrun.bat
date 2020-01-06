set PYROOT=c:\py15

PATH %PYROOT%;%PATH%

set PYTHONPATH=.;%PYROOT%;%PYROOT%\lib;%PYROOT%\lib\plat-win;%PYROOT%\lib\lib-tk;%PYROOT%\PIL;%PYROOT%ext\pyds;%PYROOT%ext\lib;
set TCL_LIBRARY=%PYROOT%\tcl8.0\library
set TK_LIBRARY=%PYROOT%\tk8.0\library

python %1
