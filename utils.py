import inspect
import re
def headerParse(header):
    return re.sub(r'[^A-Za-z0-9]+', '', header)

def isdebugging():
    for frame in inspect.stack():
        if frame[1].endswith("pydevd.py"):
            return True
    return False
