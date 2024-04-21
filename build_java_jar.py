from pathlib import Path
import os
import orekit_jpype
import jpype
import subprocess
import glob


def build_jar():
    # Get the path to the original JAR files, used for compiling
    jar_path = Path(orekit_jpype.__path__[0],'jars')

    # Get a list of all JAR files in the directory
    orekit_jar_files = jar_path.glob('*.jar')

    # Create a classpath string with the JAR files separated by colons
    classpath = ':'.join(str(jar_file) for jar_file in orekit_jar_files)

    # Define the command and arguments
    command = 'javac'

    # Get a list of all Java files in the directory and its subdirectories
    java_files = glob.glob('java-src/**/*.java', recursive=True)

    # Create the arguments list with the classpath and Java files
    args = ['-classpath', classpath] + java_files

    # Run the command
    try:
        # Combine the command and arguments into one list for subprocess.run
        print(' '.join([command] + args))
        result = subprocess.run([command] + args, check=True, text=True, capture_output=True)
        # If the command was successful, you can handle the output here
        print("javac completed successfully")
        print("Output:", result.stdout)

        # Package the output files as a JAR file
        jar_name = 'custom_jars/orekit_addons.jar'
        jar_command = 'jar'
        jar_args = ['cf', jar_name, '-C', 'java-src', '.']
        jar_result = subprocess.run([jar_command] + jar_args, check=True, text=True, capture_output=True)
        print("JAR file created successfully")
        print("Output:", jar_result.stdout)

    except subprocess.CalledProcessError as e:
        # Handle errors in the called executable
        print("Error:", e.stderr)
    except Exception as ex:
        # Handle other exceptions such as file not found or permissions issues
        print("An error occurred:", str(ex))

def cleanup_class_files():
    # Remove the compiled Java files
    java_files = glob.glob('java-src/**/*.class', recursive=True)
    for java_file in java_files:
        os.remove(java_file)

def cleanup_jar_file():
    # Remove the JAR file
    jar_file = 'custom_jars/orekit_addons.jar'
    if os.path.exists(jar_file):
        os.remove(jar_file)

if __name__ == '__main__':
    cleanup_class_files()
    cleanup_jar_file()
    build_jar()
    cleanup_class_files()

