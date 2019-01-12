r"""
Made by Alex Scorza
Using Cx_freeze and tkfilebrowser, which are automatically installed
(Good thing all of these computers have pip)
github repo = https://github.com/MegaDoot/Py-Freezer
"""

import os
import importlib
import pip


def install_lib(name_pip, name_imp):
    if importlib.find_loader(name_imp) is None:
        os.system(name_pip)
        print("Installing " + name_imp)
    exec("import " + name_imp)

##os.chdir("C:\\Program Files\\Python36")
if float(pip.__version__) < 18.1:
    os.system("python -m pip install --upgrade pip")

install_lib("pip install tkfilebrowser", "tkinter.filedialog")
install_lib("pip install Cx_freeze & Pause", "cx_Freeze")

from tkinter import filedialog as tkfd
import tkinter as tk
from tkinter import ttk

cwd = os.path.dirname(__file__)

font = "HP Simplified"
bg = "#f4c542"
fg = "#000000"
no_selection = "(None Selected)"
invalid_dir = "(Invalid Input Directory)" ##"ThIs iS DeFiNiTeLy a vAlId dIrEcToRy"

style = {
    "fg":fg,
    "bd":2
    }

btn_style = {
    "relief":"solid",
    "overrelief":"solid",
    "bg":bg,
    "font":(font, 12),
    "activebackground":"#f4b43e"
    }

entry_style = {
    "font":(font, 15),
    "width":80,
    "bg":"white",
    "relief":"solid",
    }

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(".py freezer")
        self.configure(bg = bg) #Set background of root to normal background

        ttk_style = ttk.Style() #For ttk widgets (can't use dictionary)
        ttk_style.configure("BW.TLabel", background = "white", foreground = fg, relief = "solid") #Set style to dictionary 'entry_style'

        self.sv_inputs = tuple(tk.StringVar(self, value = cwd) for x in range(2))
        
        tk.Label(text = "PY To EXE Converter", font = (font, 25), bg = bg, **style).grid(row = 0, column = 1)

        self.sv_constrain_io = tk.BooleanVar(self, value = True)
        tk.Checkbutton(self, text = "Input Dir = Output Dir", variable = self.sv_constrain_io, **style, activebackground = bg, bg = bg, font = (font, 15)).grid(row = 2, column = 1)
        
        self.entries = [tk.Entry(self, **style, **entry_style, textvariable = self.sv_inputs[0]) for x in range(2)]
        for i in range(2):
            row = 1 + (2 * i)
            self.entries[i].grid(row = row, column = 1, sticky = "NS")
            tk.Button(self, text = "Browse", **btn_style, **style, command = lambda i = i: self.set_filename(i)).grid(row = row, column = 2, sticky = "NS", padx = 5)
            tk.Label(self, text = ("Input:", "Output:")[i], font = (font, 15), bg = bg, **style).grid(row = row, column = 0, padx = 5, sticky = "E")
            self.sv_inputs[i].trace("w", lambda n, m,x: self.dir_trace())
        tk.Label(self, text = "Select A py/pyw File In Input Directory:", font = (font, 15), bg = bg, **style).grid(row = 4, column = 1)

        self.sv_file = tk.StringVar(self, value = no_selection)
        
        self.in_dir_cb = ttk.Combobox(self, textvariable = self.sv_file, style = "BW.TLabel", width = 20, font = (font, 15), state = "readonly")
        self.in_dir_cb.grid(row = 5, column = 1)

        self.build_btn = tk.Button(text = "Freeze/Build", **style, **btn_style, command = self.build)
        self.build_btn.grid(row = 6, column = 1, pady = 5)
        
        self.sv_constrain_io.trace("w", self.constraint_trace)
##
##        self.stacks = [self.sv_inputs[i].get() for i in range(2)]
##        self.stack_positions = [0] * 2

        self.bind("<Button-1>", self.flatten)
        self.bind("<<ComboboxSelected>>", lambda event: self.in_dir_cb.selection_clear())
##        self.bind("<Control-Z>", self.undo)
        self.constraint_trace()
        self.dir_trace()

##    def new_change(self, which):
##        print(self.stacks)
##        if len(self.stacks[i]) >= 10:
##            del self.stacks[i][0]
##        self.stacks[which].append(self.sv_inputs[which].get())
##
##    def undo(self, which):
##        if self.stack_positions[which] > 0:
##            self.stack_positions[which] -= 1
##        self.set_entry(which, self.stacks[which])

    def build(self):
        os.chdir(cwd)
        with open("Filename.txt", "w") as file:
            file.write(os.path.realpath(self.sv_file.get()))
        os.chdir(self.sv_inputs[not self.sv_constrain_io.get()]) #Navigate to output directory
        os.system('python "{}\\Setup.py" build'.format(cwd)) #Regardless of current directory

    def flatten(self, event):
        """By default, buttons become sunken when clicked. This is called whenever a
        button is clicked, setting it to a solid relief, only changing its background
        (see the value for "activebackground" in btn_style)"""
        if type(event.widget) == tk.Button:
            for widget in self.winfo_children():
                if type(widget) == tk.Button:
                    widget.config(relief = btn_style["relief"])

    def dir_trace(self, *args):
        """Called whenever entries updated"""
        self.sv_inputs[0].set(self.sv_inputs[0].get())
        if os.path.isdir(self.sv_inputs[0].get()):
            os.chdir(self.sv_inputs[0].get())
            self.in_dir_cb.config(values = [file for file in os.listdir() if os.path.splitext(file)[1] in (".py", ".pyw")])
            self.sv_file.set(no_selection)
        else:
            self.sv_file.set(invalid_dir)

    def constraint_trace(self, *args):
        """When checkbutton changed, the second textbox will either share a textvariable
        with the first or have its own. There are 2 possible variables - self.sv_inputs.
        If the second Entry has the first StringVar, they will remain the same. Otherwise,
        the second Entry will use the second StringVar and they will be independent."""
        self.sv_inputs[1].set(self.sv_inputs[0].get())
        self.entries[1].config(textvariable = self.sv_inputs[not self.sv_constrain_io.get()])
        
    def set_filename(self, to_set):
        """Starting from the cwd (os.path.dirname(__file__)), select a folder that contains
        a py file. The first button selects a file and the second button selects an output
        folder."""
        directory = tkfd.askdirectory(initialdir = self.sv_inputs[0].get())
        self.set_entry(to_set, directory)

    def set_entry(self, to_set, value):
        """Could alternatively be done with a setter. This is used to only set the first
        one unless Input != Output. So self.sv_inputs[1] would be ignored by default."""
        if self.sv_constrain_io.get():
            to_set = 0
        self.sv_inputs[to_set].set(value)

if __name__ == "__main__":
    app = App()
