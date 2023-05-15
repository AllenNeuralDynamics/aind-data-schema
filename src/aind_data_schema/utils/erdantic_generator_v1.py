"""Generates ERD diagrams for all modules that is a subclass AindCoreModel"""

import erdantic as erd
import glob
import os
import sys 
import inspect


os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

# python argparse

package_paths = glob.glob("**/**/**/*.py")
script_paths = glob.glob("**/**/*.py")
file_paths = package_paths + script_paths
file_paths = [x for x in file_paths if 'examples' not in x if 'tests' not in x if 'doc_template' not in x if 'src' in x]
file_paths = [x.replace('\\', '.') for x in file_paths]
file_paths = [x.replace('.py', '') for x in file_paths]

for f in file_paths:
    mod = __import__(f, fromlist=[f])
    to_import = [getattr(mod, x) for x in dir(mod)]
               # if isinstance(getattr(mod, x), type)]  # if you need classes only

    for i in to_import:
        try:
            setattr(sys.modules[__name__], i.__name__, i)
        except AttributeError:
            pass


def find_core_classes():
    """Searches for all imported classes which utilize the AindCoreModel class, and returns those modules in a list"""

    core_classes = [] # temp list
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj): # for all classes

            # Assess string for relevant info (ignore irrelevant classes)
            if 'aind_data_schema' not in obj.__module__:
                continue
            if 'datetime' in obj.__name__:
                continue

            
            argstring = inspect.getsource(obj) # Get lines of code for module

            # TODO: Make this split on first newline char, instead of ':'
            declaration = argstring.split(':')[0] # Split off first line (class declaration)

            if '(' not in declaration: # Drop anything that is not an object
                continue
            args = declaration.split('(')[1] # Take arguments
            
            if 'AindCoreModel' in args: # Check if AindCoreModel in Arguments
                core_classes.append(obj) # If yes, append to holder list
        
    return core_classes # Return 


modules = find_core_classes()


for module in modules:
    diagram = erd.create(module)
    diagram.draw("ERD_diagrams/" + module.__name__ + '.png')