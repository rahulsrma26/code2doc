import argparse
from typing import List


class ConfigOption:

    @staticmethod
    def get_short_n_full_form(option: str) -> str:
        full = '_'.join(option.strip().split())
        short = ''.join([w[0] for w in full.split('_')])
        return '-' + short, '--' + full

    def __init__(self, option: str, default, doc: str = ''):
        self.short, self.full = ConfigOption.get_short_n_full_form(option)
        self.default = default
        self.doc = doc

    def __str__(self):
        return f'{self.short:4} {self.full}  default={repr(self.default)}  doc={repr(self.doc)}'

    def add_argument(self, parser):
        if isinstance(self.default, bool): 
            if self.default is True:
                parser.add_argument(self.short, self.full, action='store_false', help=self.doc)
            else:
                parser.add_argument(self.short, self.full, action='store_true', default=False, help=self.doc)
        elif isinstance(self.default, list): 
            parser.add_argument(self.short, self.full, action='append', help=self.doc)
        else:
            parser.add_argument(self.short, self.full, default=self.default, help=self.doc)


class Configuration:

    def __init__(self):
        self.options = {}

    def add(self, option: ConfigOption):
        if option.short in self.options:
            print(f'WARNING! option {option.full} already exists in config ({option.short}). Overriding!')
        self.options[option.short] = option
        return self

    def __str__(self):
        return '\n'.join([str(o) for o in self.options.values()])

    def add_arguments(self, parser):
        for option in self.options.values():
            option.add_argument(parser)


DEFAULT_CONFIG = Configuration().add(
    ConfigOption('ignore_non_documented', False, 'Ignore files that contains no top level documentation')).add(
    ConfigOption('generate_root_directories', True, 'Generate directory for each file/module in the output directory')).add(
    ConfigOption('show_relative_imports', True, 'Show all the relative imports in a file')).add(
    ConfigOption('link_relative_imports', False, 'Link all the relative imports in a file')).add(
    ConfigOption('show_module_variables', True, 'Show all the variables in a module')).add(
    ConfigOption('show_module_functions', True, 'Show all the functions in a module')).add(
    ConfigOption('show_module_classes', True, 'Show all the classes in a module')).add(
    ConfigOption('show_class_variables', True, 'Show all the variables in a class')).add(
    ConfigOption('show_class_functions', True, 'Show all the object functions in a class')).add(
    ConfigOption('show_classmethods', True, 'Show all the classmethods of a class')).add(
    ConfigOption('show_staticmethods', True, 'Show all the staticmethods of a class')).add(
    ConfigOption('show_types', True, 'Show types in the function signature')).add(
    ConfigOption('link_types', False, 'Link types in the function signature')).add(
    ConfigOption('ignore_dot', True, 'Ignore all the files starting with a dot (hidden files)')).add(
    ConfigOption('ignore_underscore', True, 'Ignore all the files starting with an underscore')).add(
    ConfigOption('ignore_files', [], 'Ignore the specified file(s)')).add(
    ConfigOption('header_file', '', 'Append all the markdown with this in the beginning')).add(
    ConfigOption('footer_file', '', 'Append all the markdown with this in the end')).add(
    ConfigOption('build_version', True, 'Write build utility version at the end of markdown'))


if __name__ == "__main__":
    # print(DEFAULT_CONFIG)
    parser = argparse.ArgumentParser(prog='Test', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    DEFAULT_CONFIG.add_arguments(parser)
    parser.print_help()
