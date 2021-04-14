#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  This file is part of "github actions gui" project
#
#  Author: Roman Gladyshev <remicollab@gmail.com>
#  License: MIT License
#
#  SPDX-License-Identifier: MIT
#  License text is available in the LICENSE file and online:
#  http://www.opensource.org/licenses/MIT
#
#  Copyright (c) 2020 remico

import platform
from pathlib import Path

import setuptools


sources_dir = 'src'

if 'linux' not in platform.system().lower():
    raise OSError('The package requires GNU Linux. Aborting installation...')


def version():
    return Path(sources_dir, "actions_gui/VERSION").read_text()


def data_files():
    files = [str(f) for f in Path(sources_dir, "data").glob("*") if f.is_file()]
    return [('actions_gui-data', files)]


def long_description():
    return Path("README.md").read_text()


# make the distribution platform dependent
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
            # self.plat_name_supplied = True
            # self.plat_name = "manylinux1_x86_64"
except ImportError:
    bdist_wheel = None


setuptools.setup(
    name="actions_gui",
    version=version(),
    author="remico",
    author_email="remicollab@gmail.com",
    description="simple ui for a limited set of github actions",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/remico/actions",
    project_urls={
        "Source Code": "https://github.com/remico/actions",
        "Documentation": "https://github.com/remico/actions/wiki"
    },
    packages=setuptools.find_packages(where=sources_dir,
                                      exclude=['sndbx']),
    package_dir={
        '': sources_dir
    },
    package_data={
        '': ['VERSION',
             'ui/*',
             'ui/*/*',
             'assets/*']
    },
    data_files=data_files(),
    # py_modules=[],
    # register executable <command>=<pkg>.<module>:<attr>
    entry_points={
        'gui_scripts': ['ghactions = actions_gui.main:main']
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.8',
    install_requires=[
        # 'pyside6',
        # 'requests',
        # 'json2xml',
    ],
    license='MIT',
    platforms=['POSIX'],
    cmdclass={'bdist_wheel': bdist_wheel},
)
