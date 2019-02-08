"""Module"""

import os.path as op

def filedir(sys_lib, file):
    if getattr(sys_lib, "frozen", False):
        return op.dirname(sys_lib.executable)
    else:
        return op.dirname(op.realpath(file))
