import erdantic as erd
from modulefinder import ModuleFinder
import glob
import pprint
import os
import sys
import importlib

from src.aind_data_schema.behavior.behavior_rig import *
# from src.aind_data_schema.behavior.behavior_session import *
# from src.aind_data_schema.ephys.ephys_rig import *
# from src.aind_data_schema.ephys.ephys_session import *
# from src.aind_data_schema.imaging.

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

package_paths = glob.glob("**/**/**/*.py")
script_paths = glob.glob("**/**/*.py")
file_paths = package_paths + script_paths
file_paths = [x for x in file_paths if 'examples' not in x if 'tests' not in x if 'doc_template' not in x if 'src' in x]
file_paths = [x.replace('\\', '.') for x in file_paths]
file_paths = [x.replace('.py', '') for x in file_paths]

# dir_path = os.path.dirname(os.path.abspath(__file__))
# files_in_dir = [f[:-3] for f in os.listdir(dir_path)
#                 if f.endswith('.py') and f != '__init__.py']

# for f in file_paths:
#     print(f)
#     importlib.import_module(f)


for f in file_paths:
    mod = __import__(f, fromlist=[f])
    to_import = [getattr(mod, x) for x in dir(mod)]
               # if isinstance(getattr(mod, x), type)]  # if you need classes only

    for i in to_import:
        try:
            setattr(sys.modules[__name__], i.__name__, i)
        except AttributeError:
            pass

# modules = [BehaviorRig, BehaviorSession]

# print(BehaviorRig.__name__)


import sys, inspect
from inspect import signature
def find_core_classes():
    core_classes = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            # print('module: ',obj.__module__)
            if 'aind_data_schema' not in obj.__module__:
                continue
            if 'datetime' in obj.__name__:
                continue
            argstring = inspect.getsource(obj)
            declaration = argstring.split(':')[0]
            if '(' not in declaration:
                continue
            args = declaration.split('(')[1]
            
            if 'AindCoreModel' in args:
                core_classes.append(obj)
        
    return core_classes

modules = find_core_classes()

for module in modules:
    diagram = erd.create(module)
    diagram.draw("ERD_diagrams/" + module.__name__ + '.png')

# ignore = ['sys','glob','']

# dummy = 10

# output = dir()
# print(output)
# output = [x for x in output if '_' not in x]
# print(output)


# finder = ModuleFinder()
# import os 
# cwd = os.path.dirname(os.path.abspath(__file__))
# print(cwd)
# modules_fp = glob.glob('src\\aind_data_schema\\device.py')
# print(modules_fp)
# finder.run_script(modules_fp[0])

# for name, mod in finder.modules.items():
#     print(name)


