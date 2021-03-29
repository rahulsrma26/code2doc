'''
## Builder module

Responsible for Extracting functions and classes from the source.
'''

import os
from glob import glob
from .doc_types import DocModule
from .build_config import Options, Configuration
from .constants import README, OUTPUT_EXT


class DocNode:
    def __init__(self, path: str, name: list, is_file: bool, package: str, config: Configuration):
        self.name = name
        self.package = package
        import_string = '.' + '.'.join(name)
        self.module = DocModule.from_path(path, package, import_string)
        self.is_file = is_file
        self.target = package if config[Options.GENERATE_ROOT_DIRECTORIES] else ''
        if ''.join(name):
            self.target = os.path.join(self.target, os.path.sep.join(name))
        if not is_file:
            self.target = os.path.join(self.target, README)
        self.target += OUTPUT_EXT
        self.children = []

    def add(self, node):
        if node:
            self.children.append(node)

    def __str__(self):
        tag = 'f' if self.is_file else 'D'
        parts = [f'{tag} {self.name} {self.target}']
        for child in self.children:
            parts.append(str(child))
        return '\n'.join(parts)


class DocBuilder:
    ''' Document Extractor class '''
    def __init__(self, module_path: str, config: Configuration):
        ''' constructor '''
        self.path = module_path
        self.config = config
        self.abspath = os.path.abspath(self.path)
        self.basedir = os.path.dirname(self.abspath)
        self.package, _ = os.path.splitext(os.path.basename(self.abspath))
        print(self.abspath, self.basedir, self.package)
        self.tree = self.build_tree(self.abspath)

    def filter(self, name: str) -> bool:
        filename = name.split(os.path.sep)[-1]
        if self.config[Options.IGNORE_DOT_FILES] and filename.startswith('.'):
            return False
        if self.config[Options.IGNORE_UNDERSCORE_FILES] and filename.startswith('_'):
            return False
        return True

    def build_tree(self, path: str) -> DocNode:
        if os.path.isfile(path):
            base, ext = os.path.splitext(path)
            if ext == '.py':
                name = base[len(self.abspath) + 1:]
                if self.filter(name):
                    return DocNode(
                        path=self.basedir, name=name.split(os.path.sep),
                        is_file=True, package=self.package, config=self.config)
        elif os.path.isdir(path):
            if glob(os.path.join(path, "**", "*.py"), recursive=True):
                name = path[len(self.abspath) + 1:].split(os.path.sep)
                root = DocNode(
                    path=self.basedir, name=name,
                    is_file=False, package=self.package, config=self.config)
                for filename in os.listdir(path):
                    filepath = os.path.join(path, filename)
                    root.add(self.build_tree(filepath))
                return root
