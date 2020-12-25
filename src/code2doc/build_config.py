'''
Default config options for build i.e. default values for `code2doc.ini`.
'''

from .constants import PROGRAM_NAME
from .configurer import Configuration, ConfigOption


BUILD_CONFIG = Configuration(PROGRAM_NAME).add(
    ConfigOption('modules', [], 'A list of files/directories to generate documentation')).add(
    ConfigOption('output_directory', './docs', 'Output directory where markdowns will be generated')).add(
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


import os
import argparse

if __name__ == "__main__":
    # print(DEFAULT_CONFIG)
    parser = argparse.ArgumentParser(prog='Test', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    BUILD_CONFIG.add_arguments(parser)
    parser.print_help()
    # fname = os.path.join(os.path.dirname(__file__), 'default.ini')
    # BUILD_CONFIG.save(fname)
    # BUILD_CONFIG.load(fname)
    # print(DEFAULT_CONFIG)
