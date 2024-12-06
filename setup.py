from cx_Freeze import setup, Executable

build_options = {
    'packages': ['pygame'],
    'include_files': ['images', 'sounds']
}

executables = [
    Executable("main.py", base="Win32GUI")
]

setup(
    name="Truco Paulista game",
    options={'build_exe': build_options},
    executables=executables
)
