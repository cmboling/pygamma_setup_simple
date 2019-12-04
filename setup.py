
#!/usr/bin/env python

"""
setup.py file for pygamma

Author: Eric Hughes

Description

This setup.py file takes the pygamma/gamma source code found on the VESPA website
and creates the pygamma module using a simple setup.py file. The setup.py file
has been tested on windows 10 and ubuntu linux. It has been updated to work with 
python 3. Some of the updates to the source code used in this version may make it 
incompatible with python 2.7

For more informatrion on pygamma/gamma look at the original paper and the VESPA
web site https://scion.duhs.duke.edu/vespa/

"Computer Simulations in Magnetic Resonance.
An Object Oriented Programming Approach",
S.A. Smith, T.O. Levante, B.H. Meier, and R.R. Ernst,
Journal of Magnetic Resonance, 106a, 75-105, (1994). 

"""

from distutils.core import setup, Extension
import os
import sys
import numpy
from typing import Any

if __name__ == "__main__":

    # Setup  path to src and MakeMod file in order to extract pygamma c++ files

    path_base = os.path.join(os.path.abspath(os.path.curdir), 'src' )

    makemods_file = os.path.join( os.path.abspath(os.path.curdir), 'make', 'MakeMods' )

    # Read in MakeMod file

    all_lines = []
    with open(makemods_file, 'r') as file:
        for line in file:
            all_lines.append(line.strip())

    # Extract pygamma c++ files into a dictionary that includes the module 
    # directory and the list of c++ files without
    # the extension

    pygamma_files = {}

    for i,line in enumerate(all_lines):
        if '----' in line:
            module, directory = (all_lines[i-1].replace('=', "")).split()

            pygamma_files[module] = {}
            pygamma_files[module]['dd'] = directory

            k=1
            cfiles_str = all_lines[i+k]

            while all_lines[i+k][-1] == '\\':
                k +=1
                cfiles_str += all_lines[i+k]

            pygamma_files[module]['cc']=(cfiles_str.replace("\\",  " ")).split('=')[1].split()

#    [setup_py_directory, filename] = os.path.split(__file__)

    # Find the numpy include header files

    numpy_include1 = numpy.get_include()
    numpy_include2 = os.path.join( numpy_include1, 'numpy')

    # Setup the includes list for pygamma to be handed to the setup file 
    # and also the list of c++ files plus the pygamma.i file

    cfileslist = [os.path.join(path_base,'pygamma.i'),]
    skip_files = ["none"]
    includefileslist = [numpy_include1,numpy_include1, 
                        os.path.join(os.path.abspath(os.path.curdir),'src' )]

    # Work through the dictionary of c++ files and directories and create a list 
    # of c++ files with their paths

    for m in pygamma_files.keys():
        print(m)

        includefileslist.append(os.path.join( path_base, pygamma_files[m]['dd'] ))

        for cfiles in pygamma_files[m]['cc']:
            c_filepath = os.path.join(path_base, pygamma_files[m]['dd'], cfiles + '.cc' )
            if not os.path.exists(c_filepath):
                print("\n*********************")
                print('File:', c_filepath, 'does not exist')
                print("***********************\n")
            elif cfiles not in skip_files:
                cfileslist.append(c_filepath)
            else:
                print("\n*********************")
                print("skipping "+ cfiles)
                print("***********************\n")

    # Decide which operating system we are on and use the appropriate compiler flags

    if "win32" in sys.platform.lower():
        pygamma_module = Extension('_pygamma',
                                    sources= cfileslist,
                                    swig_opts= ['-c++',],
                                    include_dirs=includefileslist,
                                    extra_compile_args = [],
                                    )
    elif "linux" in sys.platform.lower():
        pygamma_module = Extension('_pygamma',
                                   sources=cfileslist,
                                   swig_opts=['-c++', ],
                                   include_dirs=includefileslist,
                                   extra_compile_args=[],
                                   )

    # Start the build/install  process

    setup(name = 'pygamma',
           version = '0.1',
           author      = ["Scott Smith", ],
           author_email = "",
           description = """pygamma""",
	       keywords="pygamma NMR python simulation",
	       license="",
           ext_modules = [pygamma_module],          
           py_modules = ["pygamma"]
           )

    # if python setup.py build command used and successful 
    # copy pygamma.py to root directory so that the
    # python setup.py install can find it

    if "win32" in sys.platform.lower():
        os.system("copy " + os.path.join(path_base,"pygamma.py") + " .")
    if "linux" in sys.platform.lower():
        os.system("cp " + os.path.join(path_base,"pygamma.py") + " .")
