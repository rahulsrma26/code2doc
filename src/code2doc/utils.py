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


def reindent(s: str, min_spaces: int = 0, trim_lines: bool = True) -> str:
    '''
    This reindents text by keeping only the minimum level of indentation.

    * s: str  
        markdown text which is needed to be reindented.
    * min_spaces: int  
        minimum number of spaces to be added as a prefix after reindentation.
    '''
    lines, m = s.splitlines(True), -1
    start = end = -1
    for idx, line in enumerate(lines):
        if not line.isspace():
            indent = len(line) - len(line.lstrip())
            m = min(m, indent) if m >= 0 else indent
            end = idx
        elif start == idx - 1:
            start = idx
    if m:
        lines = [l if l.isspace() else l[m:] for l in lines]
    prefix = ' ' * min_spaces
    if trim_lines:
        lines = lines[start + 1: end + 1]
        if lines and lines[-1]:
            lines[-1] = lines[-1].rstrip()
    return ''.join([prefix + l for l in lines])
