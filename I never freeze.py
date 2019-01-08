r"""
Made by Alex Scorza
Using Cx_freeze and tkfilebrowser, which are automatically installed
(Good thing all of these computers have pip)
"""

import os
import importlib

if importlib.find_loader("tkinter.filedialog") is None:
    os.system("pip install tkfilebrowser")
    print("Installed tkfilebrowswer")

from tkinter import filedialog as tkfd
import tkinter as tk

os.system("pip install Cx_freeze")
print("Installed Cx_freeze")

font = "Consolas"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(".py freezer")
        self.dir_entry = tk.Entry(self, font = (font, 20))

    def set_filename(self):
        self.file_name = tkfd.askopenfilename(initialdir = "S:\\", filetypes = (("python files", "*.py"), ("all files", "*.*")))

if __name__ == "__main__":
    App()
