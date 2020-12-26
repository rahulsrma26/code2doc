'''
# Extractor module

Responsible for Extracting functions and classes from the source.
'''

import os
import sys
from glob import glob
import json
from .doc_types import DocModule


class DocNode:
    def __init__(self, path:str, name: list, is_file: bool, package: str):
        self.name = name
        self.package = package
        import_string = '.' + '.'.join(name)
        self.module = DocModule.from_path(path, package, import_string)
        self.is_file = is_file
        self.children = []

    def add(self, node):
        if node:
            self.children.append(node)

    def __str__(self):
        tag = 'f' if self.is_file else 'D'
        parts = [f'{tag} {self.name}']
        for child in self.children:
            parts.append(str(child))
        return '\n'.join(parts)


class DocBuilder:
    ''' Document Extractor class '''
    def __init__(self, module_path, config):
        ''' constructor '''
        self.path = module_path
        self.config = config
        self.abspath = os.path.abspath(self.path)
        self.basedir = os.path.dirname(self.abspath)
        self.package, _ = os.path.splitext(os.path.basename(self.abspath))
        print(self.abspath, self.basedir, self.package)
        self.tree = self.build_tree(self.abspath)

    def filter(self, name):
        if self.config['ignore_dot'] and name.startswith('.'):
            return False
        if self.config['ignore_underscore'] and name.startswith('_'):
            return False
        return True

    def build_tree(self, path: str) -> DocNode:
        if os.path.isfile(path):
            base, ext = os.path.splitext(path)
            if ext == '.py':
                name = base[len(self.abspath) + 1:]
                if self.filter(name):
                    return DocNode(self.basedir, name.split(os.path.sep), is_file=True, package=self.package)
        elif os.path.isdir(path):
            if glob(os.path.join(path, "**", "*.py"), recursive=True):
                name = path[len(self.abspath) + 1:].split(os.path.sep)
                root = DocNode(self.basedir, name, is_file=False, package=self.package)
                for fname in os.listdir(path):
                    filepath = os.path.join(path, fname)
                    root.add(self.build_tree(filepath))
                return root


if __name__ == "__main__":
    config = {
        "ignore_dot": True,
        "ignore_underscore": True
    }

    builder = DocBuilder('./src/code2doc', config)
    print(builder.package)
    print(builder.tree)
