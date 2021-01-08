'''
# Extractor module

Responsible for Rendering the markdown files.
'''

import os
from glob import glob
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
        dir_name = os.path.dirname(path)
        os.makedirs(dir_name, exist_ok=True)
        print('rendering', path)
        with open(path, 'w') as f:
            f.write(self.header)
            if node.module.doc:
                f.write(node.module.doc)
            f.write(self.get_substructure(node))
            f.write(self.footer)

    def get_files_and_folders(self, node: DocNode) -> Tuple[List, List]:
        files, folders = [], []
        for child in node.children:
            if child.is_file:
                files.append((child.name, child))
            else:
                folders.append((child.name, child))
        return sorted(files), sorted(folders)

    def get_link(self, node: DocNode) -> str:
        name = node.name[-1]
        if node.is_file:
            return f'[{name}]({name}{OUTPUT_EXT})'
        else:
            return f'[{name}]({name}/{README}{OUTPUT_EXT})'

    def get_substructure(self, node: DocNode) -> str:
        files, folders = self.get_files_and_folders(node)
        s = ''
        if folders:
            rows = '\n'.join(['* ' + self.get_link(x[1]) for x in folders])
            s += f'\nFolders: \n{rows}\n'
        if files:
            rows = '\n'.join(['* ' + self.get_link(x[1]) for x in files])
            s += f'\nFiles: \n{rows}\n'
        return s


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
