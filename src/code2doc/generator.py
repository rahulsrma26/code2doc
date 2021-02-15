'''
# Generator module

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
        self.generate(builder.tree)

    def generate(self, node: DocNode):
        self.renderer.render(node)
        for child in node.children:
            self.generate(child)


from .build_config import BUILD_CONFIG

if __name__ == "__main__":
    this_dir = os.path.dirname(__file__)
    renderer = MdRenderer(BUILD_CONFIG)
    print(renderer)
    builder = DocBuilder('./src/code2doc/', BUILD_CONFIG)
    print(builder.tree)
    Generator(builder, renderer, BUILD_CONFIG)
