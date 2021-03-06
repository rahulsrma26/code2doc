'''
## Utility module

Contains different common helper functions.
'''

import os

def read_file(path: str) -> str:
    '''
    Reads a file and return it's content as a string.
    '''
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return f.read()
    else:
        return ''


def reindent(s: str, min_spaces: int = 0) -> str:
    '''
    This reindents a string by keeping only the minimum level of indentation.
    '''
    lines, m = s.splitlines(True), None
    for line in lines:
        if not line.isspace():
            indent = len(line) - len(line.lstrip())
            m = min(m, indent) if m else indent
    if m:
        lines = [l if l.isspace() else l[indent:] for l in lines]
        prefix = ' ' * min_spaces
        return ''.join([prefix + l for l in lines])
