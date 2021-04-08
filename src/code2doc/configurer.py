'''
'''
import os
import sys
import configparser
from typing import List


class ConfigOption:

    @staticmethod
    def get_short_n_full_form(option: str) -> str:
        full = '_'.join(option.strip().split())
        short = ''.join([w[0] for w in full.split('_')])
        return short, full

    def __init__(self, option: str, value, doc: str = ''):
        self.short, self.full = ConfigOption.get_short_n_full_form(option)
        self.value = value
        self.doc = doc

    def __str__(self):
        return f'{type(self).__name__}(-{self.short:4} --{self.full}  value={repr(self.value)}  doc={repr(self.doc)})'

    def add_argument(self, parser):
        short, full = f'-{self.short}', f'--{self.full}'
        if isinstance(self.value, bool):
            if self.value is True:
                parser.add_argument(short, full, action='store_false', help=self.doc)
            else:
                parser.add_argument(short, full, action='store_true', default=False, help=self.doc)
        elif isinstance(self.value, list):
            parser.add_argument(short, full, action='append', help=self.doc)
        else:
            parser.add_argument(short, full, default=self.value, help=self.doc)


class Configuration:

    def __init__(self, name):
        self.name = name
        self.shorts = {}
        self.options = []

    def add(self, option: ConfigOption):
        if option.short in self.shorts:
            print(f'WARNING! option {option.full} already exists in config ({option.short}). Overriding!')
        self.shorts[option.short] = option
        self.options.append(option)
        return self

    def __str__(self):
        title = f'{type(self).__name__}({repr(self.name)})'
        return '\n'.join([title] + [f'+--{o}' for o in self.options])

    def __getitem__(self, index):
        short, _ = ConfigOption.get_short_n_full_form(index)
        return self.shorts[short].value

    def add_arguments(self, parser):
        for option in self.options:
            option.add_argument(parser)

    def save(self, fname):
        config = configparser.ConfigParser(allow_no_value=True)
        config.add_section(self.name)
        for option in self.options:
            config.set(self.name, '; ' + option.doc)
            if isinstance(option.value, str):
                config.set(self.name, option.full, repr(option.value))
            else:
                config.set(self.name, option.full, str(option.value))
        with open(fname, 'w') as f:
            config.write(f)

    def load(self, fname):
        if not os.path.isfile(fname):
            print(f'WARNING! file `{fname}` does not exist')
            return
        config = configparser.ConfigParser()
        config.read(fname)
        if self.name in config:
            for option in self.options:
                if option.full in config[self.name]:
                    option.value = config[self.name][option.full]
                    if option.value:
                        option.value = eval(option.value)
        else:
            print(f'WARNING! section `{self.name}` does not found in `{fname}`')

    def parse(self, args):
        for option in self.options:
            specified = False
            for arg in sys.argv[1:]:
                if f'-{option.short}' in arg or f'--{option.full}' in arg:
                    specified = True
                    break
            if specified and hasattr(args, option.full):
                option.value = getattr(args, option.full)
