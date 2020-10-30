#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import getenv
from pathlib import Path

__all__ = ['path']


class path(str):
    def __new__(cls, *other):
        root = Path(__file__).parent.resolve()
        return str.__new__(cls, root.joinpath(*other))

    def join(self, *other):
        return path(Path(self).joinpath(self, *other))

    @staticmethod
    def home():
        return path(getenv('HOME'))
