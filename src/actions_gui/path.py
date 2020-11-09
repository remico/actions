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

from pathlib import Path

__all__ = ['path']


class path(str):
    def __new__(cls, *other):
        if other and Path(other[0]).is_absolute():
            fullpath = Path(*other)
        else:
            root = Path(__file__).parent.resolve()
            fullpath = root.joinpath(*other)
        return str.__new__(cls, fullpath)

    def join(self, *other):
        return path(Path(self).joinpath(self, *other))

    @staticmethod
    def home():
        return path(Path.home())
