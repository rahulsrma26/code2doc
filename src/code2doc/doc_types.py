import os
import sys
import ast
from typing import Dict, List, Tuple
from collections import defaultdict
from collections.abc import Callable
from inspect import signature, getmembers, isfunction, isclass, ismethod
from importlib import import_module, types


class DocFunction:
    def __init__(self, obj: Callable, ftype='function'):
        self.name = obj.__name__
        self.type = ftype
        self.doc = obj.__doc__
        self.signature = signature(obj)
        # self.spec = getfullargspec(obj)

    def __str__(self) -> str:
        if self.type == 'function':
            return f'{self.name}{self.signature}'
        else:
            return f'@{self.type}\n\t{self.name}{self.signature}'

    @classmethod
    def extract_from_module(cls, module: types.ModuleType) -> List['DocFunction']:
        '''
        Extract all the functions form the module object.
        '''
        for _, obj in getmembers(module, isfunction):
            if obj.__module__ == module.__name__:
                yield cls(obj)

    @classmethod
    def extract_from_class(cls, obj: object) -> Dict[str, 'DocFunction']:
        '''
        Extract all the functions form the class object.
        '''
        functions = defaultdict(list)
        for _, fobj in getmembers(obj, isfunction):
            if fobj.__name__ in  obj.__dict__:
                function_type = obj.__dict__[fobj.__name__].__class__.__name__
                functions[function_type].append(cls(fobj, function_type))
        return functions


class DocClass:
    def __init__(self, obj: object):
        self.name = obj.__name__
        self.doc = obj.__doc__
        self.base = obj.__base__ if str(obj.__base__) != str(object) else None
        self.methods = DocFunction.extract_from_class(obj)
        self.statics, classmethods = self.get_static_members(obj)
        if classmethods:
            self.methods['classmethod'] = classmethods
        self.signature = signature(obj)
        # self.spec = getfullargspec(obj)

    @staticmethod
    def get_static_members(obj: object) -> Tuple[list, list]:
        base_members = set([n for n, _ in getmembers(obj.__base__)])
        statics, classmethods = [], []
        for name, mem in getmembers(obj):
            if not name.startswith('_') and name not in base_members and not isfunction(mem):
                if ismethod(mem):
                    classmethods.append(DocFunction(mem, 'classmethod'))
                else:
                    statics.append((name, mem))
        return sorted(statics), classmethods

    def __str__(self) -> str:
        items = [f'{self.name}{self.signature}']
        statics = '\n'.join([f'\t{k} = {v}' for k, v in self.statics])
        if statics:
            items.append(statics)
        for _, methods in self.methods.items():
            items.append('\n'.join([f'\t{f}' for f in methods]))
        return '\n'.join(items)

    @classmethod
    def extract_from_module(cls, module: types.ModuleType) -> List['DocClass']:
        for _, obj in getmembers(module, isclass):
            if obj.__module__ == module.__name__:
                yield cls(obj)


class DocModule:
    def __init__(self, obj: types.ModuleType):
        self.name = obj.__name__
        self.doc = obj.__doc__
        self.imports = DocModule.get_imports(obj)
        self.functions = list(DocFunction.extract_from_module(obj))
        self.classes = list(DocClass.extract_from_module(obj))
        self.globals = DocModule.get_globals(obj, self.imports, self.functions, self.classes)

    def __str__(self):
        s = f'Module [{self.name}]\n'
        if self.globals:
            s += f'variables:\n'
            for k, v in self.globals:
                s += f'\t{k} = {v}\n'
        if self.functions:
            s += f'functions:\n'
            for func in self.functions:
                s += f'\t{func}\n'
        if self.classes:
            s += f'classes:\n'
            for c in self.classes:
                lines = '\n'.join([f'\t{l}' for l in str(c).split('\n')])
                s += f'{lines}\n'
        return s

    def get_import_group(self) -> dict:
        imports = {}
        for k, v in self.imports.items():
            if v in imports:
                imports[v].append(k)
            else:
                imports[v] = [k]
        return imports

    @staticmethod
    def get_imports(module: types.ModuleType) -> dict:
        names = {}
        if module.__file__ is None:
            print(f'Info: Module "{module.__name__}" doesn\'t have an __init__ file. '
                'Module level documentation can be added in the __init__ file.')
            return names
        # members = getmembers(module)
        with open(module.__file__) as fh:
            root = ast.parse(fh.read(), module.__file__)
            for node in ast.iter_child_nodes(root):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        names[n.name] = ''
                elif isinstance(node, ast.ImportFrom):
                    for n in node.names:
                        names[n.name] = node.module
        return names

    @staticmethod
    def get_globals(module: types.ModuleType, imports: dict, *args):
        exclude = set()
        for arg in args:
            for obj in arg:
                exclude.add(obj.name)
        variables = []
        for item, value in getmembers(module):
            if not item.startswith('_') and item not in imports and item not in exclude:
                variables.append((item, value))
        return variables

    @classmethod
    def from_path(cls, path: str, package: str, name: str = ''):
        old_path = sys.path[0]
        sys.path[0] = os.path.abspath(path)
        module = import_module(name, package) if name else import_module(package)
        sys.path[0] = old_path
        return cls(module)


if __name__ == "__main__":
    print(DocModule.from_path('./src', 'code2doc', '.doc_types'))
