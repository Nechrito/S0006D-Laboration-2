from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {"packages": ["src", "os", "pygame", "pytmx"], "include_files": ["resources"]}
exe_options = Executable(script="main.py", targetName="S0006D Pathfinding", base="Win32GUI", icon="resources/icon/Game.ico")

setup(name = "S0006D Pathfinding",
      version = "2.5",
      description = "Author: Philip Lindh",
      install_icon="resources/icon/Game.ico",
      options = {"build_exe": build_options},
      executables = [exe_options])