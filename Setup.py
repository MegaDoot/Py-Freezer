"""
Edited and adapted from:
https://pythonprogramming.net/converting-python-scripts-exe-executables/

This program is intended to be run on the command line with one argument
"""


from cx_Freeze import setup, Executable
import os

os.environ["TCL_LIBRARY"] = os.environ["TK_LIBRARY"] = r"C:\Users\alexs\Desktop\Non-Game Applications\Coding\Cmder\vendor\git-for-windows\mingw64\lib\tcl8.6"

filename = open("Filename.txt")

setup(name = "Test",
      version = "0.1" ,
      description = "" ,
      executables = [Executable("Test.py")])
