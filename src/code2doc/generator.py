'''
## Generator module

Responsible for generating the documents.
'''

import os

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

    def remove(self):
        self._remove(self.builder.tree)

    def _remove(self, node: DocNode):
        filepath = os.path.join(self.renderer.out_dir, node.target)
        if os.path.isfile(filepath):
            os.remove(filepath)
        for child in node.children:
            self._remove(child)
        if not node.is_file:
            dirpath = os.path.join(self.renderer.out_dir, os.path.dirname(node.target))
            if os.path.isdir(dirpath) and not os.listdir(dirpath):
                os.rmdir(dirpath)
