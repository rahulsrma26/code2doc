'''
# Extractor module

Responsible for Rendering the markdown files.
'''

import os
import sys
from glob import glob
import json
from typing import Tuple, List
from .constants import README, OUTPUT_EXT
from .builder import DocNode
from .build_config import Configuration, Options
from .utils import read_file

class MdRenderer:
    ''' Markdown renderer class '''
    def __init__(self, config: Configuration):
        ''' constructor '''
        self.config = config
        self.header = read_file(config[Options.HEADER_FILE].value)
        self.footer = read_file(config[Options.FOOTER_FILE].value)
        self.out_dir = config[Options.OUTPUT_DIRECTORY].value

    def render(self, node: DocNode):
        path = os.path.join(self.out_dir, node.target)
        print('rendering', path)
        with open(path, 'w') as f:
            f.write(self.header)
            if node.module:
                f.write(node.module.doc)
            f.write(self.footer)


from .builder import DocBuilder
from .build_config import BUILD_CONFIG

if __name__ == "__main__":
    this_dir = os.path.dirname(__file__)
    renderer = MdRenderer(BUILD_CONFIG)
    print(renderer)
    builder = DocBuilder('./src/code2doc/', BUILD_CONFIG)
    print(builder.tree)
    renderer.render(builder.tree)
    #     builder.generate('docs')
