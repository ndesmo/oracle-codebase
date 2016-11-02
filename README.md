# sqlbase

Scans all code from Oracle and stores it neatly.

Includes also the ability to do a fast and dirty replace on object references. Would work well in conjunction with a Git repository on the code base to identify changes in code before committing. 

Also included is a compiler.

Summary of items:
* sqlbase.py - Base class for connecting and initial setup
* create_scripts.py - Create all the scripts and store the codebase neatly
* replace_files.py - Quick and dirty replace of references to old object to new one as specified in settings
* compile_code.py - Compile given schemas and object types
* settings.ini - Settings file, controls actions of the script - can be overridden by passing arguments to classes
* exclusions.ini - objects to avoid compiling / replacing
