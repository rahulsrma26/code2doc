''' Module abcd docstring '''
from typing import List, Tuple
from collections.abc import Callable
from inspect import signature, getfullargspec, getmembers, isfunction, isclass, ismethod
from importlib import import_module, types
import pprint
from .constants import IMPORTED_CONSTANT

TEST_CONSTANT = 12345
''' TEST_CONSTANT docstring '''

test_variable = 'hi'
''' test_variable docstring '''

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
        for _, obj in getmembers(module, isfunction):
            if obj.__module__ == module.__name__:
                yield DocFunction(obj)

    @classmethod
    def extract_from_class(cls, obj: object) -> List['DocFunction']:
        for _, fobj in getmembers(obj, isfunction):
            if fobj.__name__ in  obj.__dict__:
                function_type = obj.__dict__[fobj.__name__].__class__.__name__
                yield DocFunction(fobj, function_type)


class DocClass:
    TEST = 'hahaha'
    def __init__(self, obj: object):
        self.name = obj.__name__
        self.doc = obj.__doc__
        self.base = obj.__base__ if str(obj.__base__) != str(object) else None
        self.statics, self.classmethods = self.get_static_members(obj)
        self.methods = DocFunction.extract_from_class(obj)
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
        methods = '\n'.join([f'\t{f}' for f in self.methods])
        if methods:
            items.append(methods)
        classmethods = '\n'.join([f'\t{f}' for f in self.classmethods])
        if classmethods:
            items.append(classmethods)
        return '\n'.join(items)

    @classmethod
    def extract_from_module(cls, module: types.ModuleType) -> List['DocClass']:
        for _, obj in getmembers(module, isclass):
            if obj.__module__ == module.__name__:
                yield DocClass(obj)


class DocModule:
    def __init__(self, obj: types.ModuleType):
        self.name = obj.__name__
        self.doc = obj.__doc__ 


def testing(a:int, b:int) -> int:
    return a + b

def generate_numbers() -> int:
    for i in range(10):
        yield i
