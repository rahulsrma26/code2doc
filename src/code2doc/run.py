'''
A simple code documentation utility for creating markdown file(s)
form the Docstrings.
'''

import os
from .constants import PROGRAM_NAME, VERSION, DEFAULT_CONFIG_FILENAME
from .build_config import BUILD_CONFIG, Options
from argparse import ArgumentParser, RawTextHelpFormatter


def main():
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
    cwd = os.getcwd()
    return os.path.join(cwd, DEFAULT_CONFIG_FILENAME)


def init(args):
    BUILD_CONFIG.save(get_config_path())


def clean(args):
    config = BUILD_CONFIG
    config.load(get_config_path())
    print(config[Options.OUTPUT_DIRECTORY].value)


def build(args):
    '''
    Build the docs by generating markdown files. Options can be passed
    via command-line args or by code2doc.ini file. Preference is:
    comman-line args > code2doc.ini > default command-line args
    '''
    config = BUILD_CONFIG
    config.load(get_config_path())
    config.parse(args)
    print(config)


if __name__ == "__main__":
    main()
