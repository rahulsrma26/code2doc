'''
## Renderer module

Responsible for Rendering the markdown files.
'''

import os
from typing import Tuple, List
from ..constants import README, OUTPUT_EXT
from ..builder import DocNode
from ..build_config import Configuration, Options
from ..doc_types import DocClass, DocFunction, DocModule
from ..utils import read_file, reindent
from .class_renderer import ClassRenderer
from .function_renderer import FunctionRenderer


class MdRenderer:
    ''' Markdown renderer class '''
    def __init__(self, config: Configuration, rootpath: str):
        '''
        constructor
        '''
        self.config = config
        self.rootpath = rootpath
        self.header = read_file(config[Options.HEADER_FILE])
        self.footer = read_file(config[Options.FOOTER_FILE])
        self.out_dir = config[Options.OUTPUT_DIRECTORY]
        self.class_renderer = ClassRenderer(config)
        self.function_renderer = FunctionRenderer(config)

    def render(self, node: DocNode):
        path = os.path.join(self.out_dir, node.target)
        dir_name = os.path.dirname(path)
        os.makedirs(dir_name, exist_ok=True)
        print('rendering', path)
        with open(path, 'w') as f:
            f.write(self.header)
            if self.config[Options.MODULE_NAME_HEADING]:
                name = ".".join(node.name)
                if not name:
                    name = node.package
                f.write(f'# {name} \n')
            if node.module.doc:
                f.write(node.module.doc)
                f.write('\n---\n')
            f.write(self.get_substructure(node))
            f.write(self.get_module_elements(node))
            f.write(self.footer)

    def get_files_and_folders(self, node: DocNode) -> Tuple[List, List]:
        files, folders = [], []
        for child in node.children:
            if child.is_file:
                files.append((child.name, child))
            else:
                folders.append((child.name, child))
        return sorted(files), sorted(folders)

    def get_link(self, node: DocNode) -> str:
        name = node.name[-1]
        if node.is_file:
            return f'[{name}]({name}{OUTPUT_EXT})'
        else:
            return f'[{name}]({name}/{README}{OUTPUT_EXT})'

    def get_substructure(self, node: DocNode) -> str:
        files, folders = self.get_files_and_folders(node)
        s = ''
        if folders:
            rows = '\n'.join(['* ' + self.get_link(x[1]) for x in folders])
            s += f'\nFolders: \n{rows}\n'
        if files:
            rows = '\n'.join(['* ' + self.get_link(x[1]) for x in files])
            s += f'\nFiles: \n{rows}\n'
        return s

    def get_import_group(self, all_imports: dict) -> dict:
        imports = {}
        for k, (v, f) in all_imports.items():
            if v in imports:
                imports[v].append((k, f))
            else:
                imports[v] = [(k, f)]
        filtered = {}
        for h, i in imports.items():
            relative, items = False, []
            for o, f in i:
                if self.rootpath in f:
                    relative = True
                items.append(o)
            if relative:
                filtered[h] = items
        return filtered

    def get_module_import_list(self, module: DocModule) -> str:
        imports = self.get_import_group(module.imports).items()
        if not imports or not self.config[Options.SHOW_RELATIVE_IMPORTS]:
            return ''
        s = '\nDependencies: \n'
        for k, v in imports:
            if not k:
                for i in v:
                    s += f'* import {i} \n'
            else:
                s += f'* from {k} import {", ".join(v)} \n'
        return s

    def get_module_global_list(self, module: DocModule) -> str:
        variables = module.globals
        if not variables or not self.config[Options.SHOW_MODULE_VARIABLES]:
            return ''
        s = '\nGlobals:  \n'
        for _, expr in variables:
            s += f'*   ```py\n{reindent(expr, 4)}\n    ``` \n'
        return s

    def get_module_function_list(self, module: DocModule) -> List[DocFunction]:
        if not module.functions or not self.config[Options.SHOW_MODULE_FUNCTIONS]:
            return []
        order = dict(zip(module.function_order, range(len(module.function_order))))
        if self.config[Options.KEEP_MODULE_FUNCTION_ORDER]:
            return sorted(module.functions, key=lambda x: order[x.name])
        else:
            return sorted(module.functions, key=lambda x: x.name)

    def render_module_functions(self, functions: List[DocFunction], preview: bool=False) -> str:
        s = '\nFunctions: \n' if preview and functions else ''
        for func in functions:
            if preview:
                s += f'* {self.function_renderer.link(func)} \n'
            else:
                s += self.function_renderer.render(func)
                s += self.br()
        return s

    def get_module_class_list(self, module: DocModule) -> List[DocClass]:
        if not module.classes or not self.config[Options.SHOW_MODULE_CLASSES]:
            return []
        classes = [x[0] for x in module.class_order]
        order = dict(zip(classes, range(len(classes))))
        if self.config[Options.KEEP_MODULE_CLASS_ORDER]:
            return sorted(module.classes, key=lambda x: order[x.name])
        else:
            return sorted(module.classes, key=lambda x: x.name)

    def render_module_classes(self, classes: DocClass, preview: bool=False) -> str:
        s = '\nClasses: \n' if preview and classes else ''
        for cls in classes:
            if preview:
                s += f'* {self.class_renderer.link(cls)} \n'
            else:
                s += self.class_renderer.render(cls)
                s += self.br()
        return s

    def br(self) -> str:
        if self.config[Options.ADD_COMPONENT_LINEBREAKS]:
            return '\n---\n'
        return ''

    def get_module_elements(self, node: DocNode) -> str:
        functions = self.get_module_function_list(node.module)
        classes = self.get_module_class_list(node.module)
        s = ''
        s += self.get_module_import_list(node.module)
        s += self.get_module_global_list(node.module)
        s += self.render_module_functions(functions, preview=True)
        s += self.render_module_classes(classes, preview=True)
        s += self.br()
        s += self.render_module_functions(functions, preview=False)
        s += self.render_module_classes(classes, preview=False)
        return s
