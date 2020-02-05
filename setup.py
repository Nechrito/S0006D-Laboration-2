from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {"packages": ["os", "pygame", "pytmx"], "include_files": ["src"]}
exe_options = Executable(script="main.py", targetName="S0006D Assignment", base="Win32GUI", icon="src/resources/icon/Game.ico")

setup(  name = "S0006D Assignment",
        version = "2.1",
        description = "Author: Philip Lindh",
        options = {"build_exe": build_options},
        executables = [exe_options])