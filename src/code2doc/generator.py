'''
## Generator module

Responsible for generating the documents.
'''

from .build_config import Configuration, Options
from .builder import DocBuilder, DocNode
from .renderer.renderer import MdRenderer


class Generator:
    ''' Document Generator class '''
    def __init__(self, builder: DocBuilder, renderer: MdRenderer, config: Configuration):
        ''' constructor '''
        self.config = config
        self.builder = builder
        self.renderer = renderer

    def generate(self):
        self._generate(self.builder.tree)

    def _generate(self, node: DocNode):
        self.renderer.render(node)
        for child in node.children:
            self._generate(child)

