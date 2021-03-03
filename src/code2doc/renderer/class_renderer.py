'''
## Class Renderer module

Responsible for Rendering the class docs in markdown file.
'''

from ..build_config import Configuration, Options
from ..doc_types import DocClass


class ClassRenderer:
    ''' Class renderer class '''
    def __init__(self, config: Configuration):
        ''' constructor '''
        self.config = config

    def link(self, cls: DocClass) -> str:
        base = ' ({cls.base.__name__})' if cls.base else ''
        return f'[{cls.name}{base}](#{cls.name})'

    def render(self, cls: DocClass) -> str:
        base = ' ({cls.base.__name__})' if cls.base else ''
        s = '\n'
        s += f'## {cls.name} {base} \n'
        s += f'{cls.doc} \n'
        if cls.classmethods:
            s += f'\nClassmethods \n'
            for obj in cls.classmethods:
                s += f'* {obj.name} {obj.signature} \n'
                s += f'{obj.doc} \n'
        return s
