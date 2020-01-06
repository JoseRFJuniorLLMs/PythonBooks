cl -c dictionary.c -I\pystuff\python-1.5.2\Include -I\pystuff\python-1.5.2\PC -I. 

link dictionary.obj \pystuff\python-1.5.2\PCbuild\python15.lib -out:dict.exe