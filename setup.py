from __future__ import absolute_import, division, print_function

import os
import sys
import platform
from setuptools import setup, find_packages

_this = os.path.abspath(os.path.dirname(__file__))

def get_requirements(filename):
    contents = open(os.path.join(_this, filename)).read()
    return [
        req for req in contents.split('\n')
        if req != '' and not req.startswith('#')
    ]

setup(
    version='0.0.2',
    install_requires=get_requirements('requirements-client.txt')
)
