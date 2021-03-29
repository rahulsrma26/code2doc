'''
## Class Renderer module

Responsible for Rendering the class docs in markdown file.
'''

from ..build_config import Configuration, Options
from ..doc_types import DocClass
from ..utils import reindent


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
        if cls.doc:
            s += f'{cls.doc} \n'
        if self.config[Options.SHOW_CLASS_METHODS]:
            for method_type, methods in cls.methods.items():
                postfix = 's' if len(methods) > 1 else ''
                s += f'\n{method_type}{postfix}: \n'
                for obj in methods:
                    name = obj.name.replace("_", "\\_")
                    s += f'* **{name}** {obj.signature} \n'
                    if obj.doc:
                        doc = reindent(obj.doc, 4) if self.config[Options.REINDENT_DOCS] else obj.doc
                        s += f'{doc} \n'
        return s
