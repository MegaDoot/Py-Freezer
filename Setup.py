"""
Edited and adapted from:
https://pythonprogramming.net/converting-python-scripts-exe-executables/

This program is intended to be run on the command line with one argument
"""


from cx_Freeze import setup, Executable
from sys import argv

setup(name = os.path.splitext(argv[0])[0] ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable(argv[0])])
