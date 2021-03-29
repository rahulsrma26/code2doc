'''
## Function Renderer module

Responsible for Rendering the function docs in markdown file.
'''

from ..build_config import Configuration, Options
from ..doc_types import DocFunction
from ..utils import reindent


class FunctionRenderer:
    ''' Function renderer class '''
    def __init__(self, config: Configuration):
        ''' constructor '''
        self.config = config

    def link(self, func: DocFunction) -> str:
        return f'[{func.name} {func.signature}](#{func.name})'

    def render(self, func: DocFunction) -> str:
        s = '\n'
        s += f'## {func.name} {func.signature} \n'
        if func.doc:
            doc = reindent(func.doc) if self.config[Options.REINDENT_DOCS] else func.doc
            s += f'{doc} \n'
        return s
