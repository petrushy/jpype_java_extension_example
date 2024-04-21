from pathlib import Path
import os
import jpype
import orekit_jpype
jpype.addClassPath('custom_jars/orekit_addons.jar')
orekit_jpype.initVM()

print(f"Java version: {jpype.getJVMVersion()}")
print(f"Java JVM path: {jpype.getDefaultJVMPath()}")
from org.orekit.time import AbsoluteDate

from org.orekit.propagation.events import NewElevationDetector
pass