
import subprocess

subprocess.call("java -jar antlr-4.7.1-complete.jar -Dlanguage=Python3 C.g4 -visitor", shell=True, cwd="src/")
subprocess.call("python3.5 -m unittest discover tests '*Test.py' -v", shell=True, cwd="src/")
