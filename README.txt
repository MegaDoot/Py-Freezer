tl;dr: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Otherwise...


Basically just open up 'I never freeze.py'
The source code is available here: https://github.com/MegaDoot/Py-Freezer
(Or just open up the files in IDLE/Notepad/Sublime/VSCode/whatever)

Cx_freeze doesn't work for Python 3.7.
If you are using this version, open up 'I never freeze.py' for further instructions.
You can follow the link and use the fix, but I recommend just using 3.5/6 because
it may cause other issues as I have not fully tested this for 3.7 due to Cx_freeze
incompatibility.

By default, 'os' is the only package included and 'tkinter' is the only file included.
3rd-party modules, like 'scipy' or 'matplotlib' as well as some included with Python
will need to be added to 'packages'. If you are having problems with 3rd-party modules,
refer to https://stackoverflow.com/questions/42078262/issue-with-matplotlib-and-cx-freeze

The program creates a folder called 'build'. Open this and open the file inside.