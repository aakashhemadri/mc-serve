#!/usr/bin/env python

import setuptools
import sys
import os
import re


if sys.version_info < (3, 0):
    print('MCServe requires at least Python 3 to run.')
    sys.exit(1)

PY3 = sys.version_info[0] == 3

# Global functions
##################

with open(os.path.join('mcserve', '__init__.py'), encoding='utf-8') as f:
    version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)

if not version:
    raise RuntimeError('Cannot find MCServe version information.')

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_data_files():
    data_files = [
        ('share/doc/compose-templates', ['docs/compose-templates/bukkit/bukkit-docker-compose.yml', 'docs/compose-templates/paper/paper-docker-compose.yml', 'docs/compose-templates/vanilla/hardcore-docker-compose.yml'] ),
        ( 'share/doc/mcserve',['AUTHORS.md', 'README.md','CONTRIBUTING.md', 'conf/mcserve.conf']),
        ('share/man/man1', ['docs/man/mcserve.1'])
    ]
    return data_files

setuptools.setup(
    name="mcserve",
    version=version,
    author="Aakash Hemadri",
    author_email="aakashhemadri123@gmail.com",
    description="docker-minecraft-server manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aakashhemadri/mcserve",
    packages=setuptools.find_packages(),
    data_files=get_data_files(),
    entry_points={"console_scripts": ['mcserve=mcserve:main']},

    classifiers=[
        'Environment :: Console :: Curses',
        'Intended Audience :: End Users/Desktop',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)