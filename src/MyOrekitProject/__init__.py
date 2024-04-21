import orekit_jpype
import os

# Get the  path of the current file, used for finding the jars directory
dirpath = os.path.dirname(os.path.abspath(__file__))

def initVM():
    additional_classpaths = os.path.join(dirpath, 'jars','orekit_addons.jar')
    orekit_jpype.initVM(additional_classpaths=[additional_classpaths])
