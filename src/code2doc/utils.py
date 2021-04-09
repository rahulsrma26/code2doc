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
    This reindents text by keeping only the minimum level of indentation.

    * s: str  
        markdown text which is needed to be reindented.
    * min_spaces: int  
        minimum number of spaces to be added as a prefix after reindentation.
    '''
    lines, m = s.splitlines(True), -1
    for line in lines:
        if not line.isspace():
            indent = len(line) - len(line.lstrip())
            m = min(m, indent) if m >= 0 else indent
    if m:
        lines = [l if l.isspace() else l[m:] for l in lines]
    prefix = ' ' * min_spaces
    return ''.join([prefix + l for l in lines])
