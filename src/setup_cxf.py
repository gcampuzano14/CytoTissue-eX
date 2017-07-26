from cx_Freeze import setup,Executable

# exe = Executable(
#     script="pis_nls_parser.py",
#     base="Win32GUI",
#     )
#
# setup(
#     name = "wxSampleApp",
#     version = "0.1",
#     description = "An example wxPython script",
#     executables = [exe]
#     )

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': ['PyQt4', 'werkzeug', 'forms', 'gevent','copathnlshack','tempfile','config', 'flask', 're', 
                     'greenlet', 'gevent.core'],
    }
}

executables = [
    Executable('pis_nls_parser.py', base=base)
]

setup(name='Copath NLS Parser',
      version='0.2',
      description='CPNLSP',
      options=options,
      executables=executables
      )
