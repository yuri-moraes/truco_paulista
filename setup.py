import cx_Freeze

executables = [cx_Freeze.Executable('main.py')]

cx_Freeze.setup(
    name="Truco Paulista game",
    options={'build_exe': {'packages':['pygame'],
                           'include_files':['images', 'sounds']}},

    executables = executables
    
)