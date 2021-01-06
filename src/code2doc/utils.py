import os

def read_file(path: str) -> str:
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return f.read()
    else:
        return ''
