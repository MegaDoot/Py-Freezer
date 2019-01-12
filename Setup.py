"""
Sources (what this was adapted from):
https://pythonprogramming.net/converting-python-scripts-exe-executables/
https://www.youtube.com/watch?v=HosXxXE24hA
https://stackoverflow.com/questions/43059408/how-to-include-tkinter-when-using-cx-freeze-to-convert-script-to-exe/43071342

https://www.youtube.com/watch?v=dQw4w9WgXcQ
"""


from cx_Freeze import setup, Executable #Setup in 'I never freeze.py'
import os
import re
import sys

dir_ = repr(open(os.path.dirname(__file__) + "\Dir.txt").read())
os.environ["TCL_LIBRARY"] = dir_ + r"\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = dir_ + r"\tcl\tk8.6"

base = None
if sys.platform == "win32":
    base = "Win32GUI"

filename = open(os.path.dirname(__file__) + "\Filename.txt").read()
name = re.compile(r"[A-Za-z]+\.py(w?)$").search(filename).group() #Get name of file only

setup(name = os.path.splitext(filename)[0],
      version = "0.1",
      description = "",
      executables = [Executable(filename, base = base)],
      options = {"build_exe":{"packages":["os"],
                              "includes":["tkinter"],
                              "include_files": [dir_ + r"\DLLs\tcl86t.dll",
                                                dir_ + r"DLLs\tk86t.dll"]
                              }
                 }
      )
