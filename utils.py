import inspect
import os
import re
def headerParse(header):
    return re.sub(r'[^A-Za-z0-9]+', '', header)

def isdebugging():
    for frame in inspect.stack():
        if frame[1].endswith("pydevd.py"):
            return True
    return False

def linenumber() -> int:
    return inspect.currentframe().f_back.f_lineno

def getFileInsensitive(dir: str, fileName: str):
    for file in os.listdir(dir):
        if file.lower() == fileName.lower():
            return file
    return None
