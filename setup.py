import cx_Freeze
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
executables = [cx_Freeze.Executable("HenPuzzle.py", base='Win32GUI')]

include_files = ["1.jpg", "background.jpg",(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll')),
                 (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll'))]

cx_Freeze.setup(
    name="Hentai Puzzle",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":include_files}},
    executables = executables

    )