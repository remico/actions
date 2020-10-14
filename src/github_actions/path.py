#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

__all__ = ['path']


class path:
    def __init__(self, *other):
        self.package_root = Path(__package__).absolute()
        self.initial_path = self.package_root.joinpath(*other)

    def __repr__(self):
        return str(self.initial_path)

    def join(self, *other):
        return self.initial_path.joinpath(*other)

    def joins(self, *other):
        return str(self.join(*other))

    def str(self):
        return self.__repr__()
