# Example of a project with custom java classes in combination with the orekit_jpype wrapper

This project is an example of how to incorporate customer java classes in a project that uses the orekit_jpype wrapper.

The possibility to incorporate custom java classes is a feature that enables to write small freqently called parts in java to improve performance. This is typically useful for event detectors or other parts that are called frequently and taking penalty from the python to java conversion.

The project takes java code in the java-src directory and compiles it into a jar file. This jar file is then included in the python project and can be accessable from the python code.

