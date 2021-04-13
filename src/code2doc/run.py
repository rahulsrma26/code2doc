'''
This is the entry point for the commands. Currently, it supports three sub-commands: init, build, and clean.
'''

import os
from .constants import PROGRAM_NAME, VERSION, DEFAULT_CONFIG_FILENAME
from .build_config import BUILD_CONFIG, Options
from .builder import DocBuilder
from .renderer.renderer import MdRenderer
from .generator import Generator
from argparse import ArgumentParser, RawTextHelpFormatter


def main():
    '''
    Entry function for the module. Create arg-parser and all of the sub-parsers.
    '''
    parser = ArgumentParser(
        PROGRAM_NAME,
        description=f'Version {VERSION}\n' + __doc__,
        formatter_class=RawTextHelpFormatter,
        epilog='Check out individual command\'s help using code2doc <command> -h\n')

    subparser = parser.add_subparsers(
        title='commands',
        description='''Usage: code2doc <command> [command-options]\n\nWhere <command> can be one of them:''')

    init_parser = subparser.add_parser(
        'init',
        description=init.__doc__,
        formatter_class=RawTextHelpFormatter,
        help=f'create or override the default config file ({DEFAULT_CONFIG_FILENAME})')
    BUILD_CONFIG.add_arguments(init_parser)
    init_parser.set_defaults(func=init)

    build_parser = subparser.add_parser(
        'build',
        description=build.__doc__,
        formatter_class=RawTextHelpFormatter,
        help='builds the markdown documentation')
    BUILD_CONFIG.add_arguments(build_parser)
    build_parser.set_defaults(func=build)

    clean_parser = subparser.add_parser(
        'clean',
        description=clean.__doc__,
        formatter_class=RawTextHelpFormatter,
        help='removes the generated markdowns in the output directory')
    clean_parser.set_defaults(func=clean)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        parser.print_help()


def get_config_path():
    '''
    Helper function that returns the config-file path in the present working directory.
    '''
    cwd = os.getcwd()
    return os.path.join(cwd, DEFAULT_CONFIG_FILENAME)


def init(args):
    '''
    This will create default code2doc.ini file in the present working directory.
    '''
    config = BUILD_CONFIG
    config.parse(args)
    config.save(get_config_path())


def clean(args):
    '''
    Removes all the doc file(s) created by the config file. It also remove
    all the empty folders in its sub-directories.
    '''
    config = BUILD_CONFIG
    config.load(get_config_path())
    print(config[Options.OUTPUT_DIRECTORY])
    for module_path in config[Options.MODULES]:
        builder = DocBuilder(module_path, config)
        print(builder.tree)
        renderer = MdRenderer(config, builder.abspath)
        print(renderer)
        Generator(builder, renderer, config).remove()


def build(args):
    '''
    Build the docs by generating markdown files. Options can be passed
    via command-line args or by code2doc.ini file.

    Preference is:  
    command-line args > code2doc.ini > default command-line args
    '''
    config = BUILD_CONFIG
    config.load(get_config_path())
    config.parse(args)
    for module_path in config[Options.MODULES]:
        builder = DocBuilder(module_path, config)
        print(builder.tree)
        renderer = MdRenderer(config, builder.abspath)
        print(renderer)
        Generator(builder, renderer, config).generate()


if __name__ == "__main__":
    main()
