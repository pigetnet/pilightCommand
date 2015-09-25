import threading
import subprocess
import time
import sys

"""
"Send commands"
"""


def sendCommandThreaded(command):
    result = subprocess.check_output([command], shell=True)
    sys.stdout.write(result)


def send(command):
    commandThread = threading.Thread(target=sendCommandThreaded, args=(command,))
    commandThread.start()
