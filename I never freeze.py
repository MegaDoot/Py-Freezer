r"""
DON'T USE PYTHON 3.7 OR ABOVE (although this error is caught)
Cx_freeze is not updated for Python 3.7.x

Made by Alex Scorza
pip and python are needed. Either set them as path variables, the setx command
or navigate to where python.exe and pip.exe are installed and run this program
from the command line.

Cx_freeze and tkfilebrowser are automatically installed, as it pip 18.2
github repo = https://github.com/MegaDoot/Py-Freezer
"""

import os, importlib, pip, re, sys

py_dir = os.__file__[:-10]
if not "Dir.txt" in os.listdir():
    with open("Dir.txt", "w") as file:
        file.write(py_dir) #Path of Python
        print("Directory Added: " + py_dir)
#(Note that any library (not just os) can be used)

os.chdir(py_dir + r"\Scripts")

def find_version(string):
    return re.compile("^\d+\.\d+").search(string).group()

def install_lib(name_pip, name_imp):
##    if importlib.util.find_spec(name_imp) is None: #If not found
##        print("Installing " + name_imp)
##        os.system(name_pip)
##    else:
##        print(name_imp + " Is Already Installed")
##        exec("import " + name_imp)
    try:
        exec("import " + name_imp)
        print(name_imp + " Is Already Installed")
    except:
        print("Installing " + name_imp)
        os.system(name_pip)
        exec("import " + name_imp)

if float(find_version(pip.__version__)) < 18.1:
    print("Installing pip 18.1")
    os.system("python -m pip install --upgrade pip")

install_lib("pip install tkfilebrowser", "tkinter.filedialog")
install_lib("pip install Cx_freeze", "cx_Freeze")

del pip, importlib

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
    "activebackground":"#f4b43e",
    "disabledforeground":"#848484",
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
        self.title(".py/.pyw freezer")
        self.configure(bg = bg) #Set background of root to normal background

        ttk_style = ttk.Style() #For ttk widgets (can't use dictionary)
        ttk_style.configure("BW.TLabel", background = "white", foreground = fg, relief = "solid") #Set style to dictionary 'entry_style'

        self.sv_inputs = tuple(tk.StringVar(self, value = cwd) for x in range(2))
        self.sv_file = tk.StringVar(self, value = no_selection)
        self.sv_constrain_io = tk.BooleanVar(self, value = True)
        
        tk.Label(text = "PY To EXE Converter", font = (font, 25), bg = bg, **style).grid(row = 0, column = 1)
        tk.Checkbutton(self, text = "Input Dir = Output Dir", variable = self.sv_constrain_io, **style, activebackground = bg, bg = bg, font = (font, 15)).grid(row = 2, column = 1)

        self.entries = [tk.Entry(self, **style, **entry_style, textvariable = self.sv_inputs[0]) for x in range(2)]
        for i in range(2):
            row = 1 + (2 * i)
            self.entries[i].grid(row = row, column = 1, sticky = "NS")
            tk.Button(self, text = "Browse", **btn_style, **style, command = lambda i = i: self.set_filename(i)).grid(row = row, column = 2, sticky = "NS", padx = 5)
            tk.Label(self, text = ("Input:", "Output:")[i], font = (font, 15), bg = bg, **style).grid(row = row, column = 0, padx = 5, sticky = "E")
            self.sv_inputs[i].trace("w", lambda n, m, x: self.dir_trace())
        self.sv_constrain_io.trace("w", self.constraint_trace)

        tk.Label(self, text = "Select A py/pyw File In Input Directory:", font = (font, 15), bg = bg, **style).grid(row = 4, column = 1)
        self.in_dir_cb = ttk.Combobox(self, textvariable = self.sv_file, style = "BW.TLabel", width = 20, font = (font, 15), state = "readonly")
        self.in_dir_cb.grid(row = 5, column = 1)
        self.build_btn = tk.Button(text = "Freeze/Build", **style, **btn_style, command = self.build, state = "disabled")
        self.build_btn.grid(row = 6, column = 1, pady = 5)
        
        self.bind("<Button-1>", self.flatten)
        self.bind("<<ComboboxSelected>>", lambda event: [self.in_dir_cb.selection_clear(), self.build_btn.config(state = ("normal" if self.valid_output() else "disabled"))])

        self.constraint_trace()
        self.dir_trace()

        self.mainloop()
        
    def build(self):
        os.chdir(cwd)
        with open("Filename.txt", "w") as file:
            input_dir = self.sv_inputs[0].get()
            file.write(input_dir + ("\\" if input_dir[-1] != "\\" else "") + self.sv_file.get())
        os.chdir(self.sv_inputs[not self.sv_constrain_io.get()].get()) #Navigate to output directory
        os.system('python "{}/Setup.py" build'.format(cwd)) #Regardless of current directory

    def valid_output(self):
        if os.path.exists(self.sv_inputs[not self.sv_constrain_io.get()].get()):
            return True
        return False

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
        self.build_btn.config(state = "disabled")
        for i in range(2):
            self.sv_inputs[i].set(self.sv_inputs[i].get().replace("/", "\\"))
        if os.path.isdir(self.sv_inputs[0].get()):
            os.chdir(self.sv_inputs[0].get())
            self.in_dir_cb.config(values = [file for file in os.listdir() if os.path.splitext(file)[1] in (".py", ".pyw")])
            self.sv_file.set(no_selection)
        else:
            self.sv_file.set(invalid_dir)
            self.in_dir_cb.config(values = [])

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

class VersionError(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Version Error")
        self.configure(bg = bg)

        import webbrowser
        
        tk.Message(**style, font = (font, 20),justify = "center", width = 500, bg = bg,
                   text = """It appears that you are using Python 3.7.
Cx_freeze (imported as cx_Freeze) is not updated for 3.7.x (13/01/19).
Please revert to 3.6 or lower or use the fix in the link below:"""
                   ).grid(row = 0, column = 0, columnspan = 2)
        url_text = tk.Text(self, font = (font, 15), state = "normal", height = 1, width = 45)
        url_text.tag_configure("center", justify = "center")
        url_text.insert("1.0", url)
        url_text.tag_add("center", "1.0", "end")
        url_text.config(state = "disabled")
        url_text.grid(row = 1, column = 0, columnspan = 2)
        commands = (self.copy, lambda: webbrowser.open(url))
        for i in range(2):
            tk.Button(**style, **btn_style, text = ("Copy To Clipboard", "Open In Browser")[i], command = commands[i]).grid(row = 2, column = i, pady = 5, padx = 5, sticky = "EW")

        self.bind("<Button-1>", self.flatten)
        self.mainloop()

    def copy(self):
        """Add the url to the clipboard"""
        self.clipboard_clear()
        self.clipboard_append(url)

    def flatten(self, event):
        """Same as flatten method for App class"""
        App.flatten(self, event)

if __name__ == "__main__":
    version = sys.version_info
    del sys
    if  version >= (3,7,0):
        url = r"https://github.com/anthony-tuininga/cx_Freeze/issues/407"
        app = VersionError()
    else:
        app = App()
