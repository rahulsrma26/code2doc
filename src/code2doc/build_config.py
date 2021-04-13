'''
Default options for building the docs. Same options are used for both 
the `code2doc.ini` file as well as the command line arguments for the 
build command.

See Also: [Configuration](configurer.md#Configuration), [ConfigOption](configurer.md#ConfigOption)
'''

from .constants import PROGRAM_NAME
from .configurer import Configuration, ConfigOption


class Options:
    '''
    Defines the string constants for the config options.
    '''
    MODULES = 'modules'
    OUTPUT_DIRECTORY = 'output_directory'
    IGNORE_NON_DOCUMENTED = 'ignore_non_documented'
    GENERATE_ROOT_DIRECTORIES = 'generate_root_directories'
    SHOW_RELATIVE_IMPORTS = 'show_relative_imports'
    LINK_RELATIVE_IMPORTS = 'link_relative_imports'
    SHOW_MODULE_VARIABLES = 'show_module_variables'
    SHOW_MODULE_FUNCTIONS = 'show_module_functions'
    KEEP_MODULE_FUNCTION_ORDER = 'keep_module_function_order'
    SHOW_MODULE_CLASSES = 'show_module_classes'
    KEEP_MODULE_CLASS_ORDER = 'keep_module_class_order'
    SHOW_CLASS_VARIABLES = 'show_class_variables'
    SHOW_CLASS_METHODS = 'show_class_methods'
    SHOW_TYPES = 'show_types'
    LINK_TYPES = 'link_types'
    IGNORE_DOT_FILES = 'ignore_dot_files'
    IGNORE_UNDERSCORE_FILES = 'ignore_underscore_files'
    IGNORE_FILES = 'ignore_files'
    HEADER_FILE = 'header_file'
    FOOTER_FILE = 'footer_file'
    BUILD_VERSION = 'build_version'
    REINDENT_DOCS = 'reindent_docs'
    ADD_COMPONENT_LINEBREAKS = 'add_component_linebreaks'
    MODULE_NAME_HEADING = 'module_name_heading'


BUILD_CONFIG = Configuration(PROGRAM_NAME).add(
    ConfigOption(Options.MODULES, [], 'A list of files/directories to generate documentation')).add(
    ConfigOption(Options.OUTPUT_DIRECTORY, './docs', 'Output directory where markdowns will be generated')).add(
    ConfigOption(Options.IGNORE_NON_DOCUMENTED, False, 'Ignore files that contains no top level documentation')).add(
    ConfigOption(Options.GENERATE_ROOT_DIRECTORIES, True, 'Generate directory for each file/module in the output directory')).add(
    ConfigOption(Options.SHOW_RELATIVE_IMPORTS, True, 'Show all the relative imports in a file')).add(
    ConfigOption(Options.LINK_RELATIVE_IMPORTS, False, 'Link all the relative imports in a file')).add(
    ConfigOption(Options.SHOW_MODULE_VARIABLES, True, 'Show all the variables in a module')).add(
    ConfigOption(Options.SHOW_MODULE_FUNCTIONS, True, 'Show all the functions in a module')).add(
    ConfigOption(Options.KEEP_MODULE_FUNCTION_ORDER, False, 'Show all the functions in the module in order of definition. On False it will show alphabetically.')).add(
    ConfigOption(Options.SHOW_MODULE_CLASSES, True, 'Show all the classes in a module')).add(
    ConfigOption(Options.KEEP_MODULE_CLASS_ORDER, False, 'Show all the classes in the module in order of definition. On False it will show alphabetically.')).add(
    ConfigOption(Options.SHOW_CLASS_VARIABLES, True, 'Show all the static variables in a class')).add(
    ConfigOption(Options.SHOW_CLASS_METHODS, True, 'Show all the methods in a class')).add(
    ConfigOption(Options.SHOW_TYPES, True, 'Show types in the function signature')).add(
    ConfigOption(Options.LINK_TYPES, False, 'Link types in the function signature')).add(
    ConfigOption(Options.IGNORE_DOT_FILES, True, 'Ignore all the files starting with a dot (hidden files)')).add(
    ConfigOption(Options.IGNORE_UNDERSCORE_FILES, True, 'Ignore all the files starting with an underscore')).add(
    ConfigOption(Options.IGNORE_FILES, [], 'Ignore the specified file(s)')).add(
    ConfigOption(Options.HEADER_FILE, '', 'Append all the markdown with this in the beginning')).add(
    ConfigOption(Options.FOOTER_FILE, '', 'Append all the markdown with this in the end')).add(
    ConfigOption(Options.BUILD_VERSION, True, 'Write build utility version at the end of markdown')).add(
    ConfigOption(Options.REINDENT_DOCS, True, 'Reindent the docs to avoid top level markdown blocks')).add(
    ConfigOption(Options.ADD_COMPONENT_LINEBREAKS, True, 'Add linebreaks after every doc component')).add(
    ConfigOption(Options.MODULE_NAME_HEADING, True, 'Adds the relative module path as heading in docs.'))
