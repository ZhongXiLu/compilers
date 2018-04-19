
import subprocess

subprocess.call("sudo pip3 install -r requirements.txt", shell=True)
subprocess.call("java -jar antlr-4.7.1-complete.jar -Dlanguage=Python3 C.g4 -visitor", shell=True, cwd="src/")
