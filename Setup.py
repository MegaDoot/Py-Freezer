"""
Sources (what this was adapted from):
https://pythonprogramming.net/converting-python-scripts-exe-executables/
https://www.youtube.com/watch?v=HosXxXE24hA
https://stackoverflow.com/questions/43059408/how-to-include-tkinter-when-using-cx-freeze-to-convert-script-to-exe/43071342

https://www.youtube.com/watch?v=dQw4w9WgXcQ
(That one was SUPER useful)
"""


from cx_Freeze import setup, Executable #Setup in 'I never freeze.py'
import os
import re
import sys
import json

file_dir = os.path.dirname(__file__) #Directory of this file
dir_ = open(file_dir + r"\Dir.txt").read() + "\\" #Python directory

os.environ["TCL_LIBRARY"] = dir_ + r"tcl\tcl8.6"
os.environ["TK_LIBRARY"] = dir_ + r"tcl\tk8.6"

base = None
if sys.platform == "win32":
    base = "Win32GUI"

filename = open(file_dir + r"\Filename.txt").read()
name = re.compile(r"[A-Za-z]+\.py(w?)$").search(filename).group() #Get name of file only

config = json.loads(open(file_dir + r"\Config.json", "r").read())
print(config)
for i in range(2): #Add prefixes to make full path
    config["include_files"][i] = dir_ + config["include_files"][i]

setup(name = os.path.splitext(filename)[0],
      version = "0.1",
      description = "",
      executables = [Executable(filename, base = base)],
      options = {"build_exe":config}
      )

