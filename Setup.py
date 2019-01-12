"""
Edited and adapted from:
https://pythonprogramming.net/converting-python-scripts-exe-executables/
"""


from cx_Freeze import setup, Executable
import os
import re

os.environ["TCL_LIBRARY"] = os.environ["TK_LIBRARY"] = r"C:\Users\alexs\Desktop\Non-Game Applications\Coding\Cmder\vendor\git-for-windows\mingw64\lib\tcl8.6"

filename = open("Filename.txt").read()
name = re.compile(r"[A-Za-z]+\.py(w?)$").search(filename).group() #Get name of file only

setup(name = os.path.splitext(filename)[0],
      version = "0.1" ,
      description = "" ,
      executables = [Executable(filename)])
