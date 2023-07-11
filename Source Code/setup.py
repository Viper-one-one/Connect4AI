from cx_Freeze import setup, Executable

base = None    

executables = [Executable("Connect4AI.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Connect 4",
    options = options,
    version = "1",
    description = 'multi-mode AI connect 4 game',
    executables = executables
)
