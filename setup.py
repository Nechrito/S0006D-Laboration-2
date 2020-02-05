import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "pygame", "pytmx"], "include_files": ["src"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "S0006D Assignment",
        version = "0.2",
        description = "Author: Philip Lindh",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Main.py", targetName="S0006D Assignment", base=base)] )