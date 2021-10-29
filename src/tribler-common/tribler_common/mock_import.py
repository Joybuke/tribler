""" A helper mocking function to mask ImportError on a scoped code.
Failed imports will be ignored.

This module has been copied from https://github.com/posener/mock-import and modified by @drew2a
to allow `mock_import` ignore only packages included to the `packages` list.

Original module distributes under Apache License 2.0.
"""
from typing import List

import mock

import six


__all__ = ['mock_import']

_builtins_import = six.moves.builtins.__import__


def mock_import(packages=List[str], **mock_kwargs):
    """
    Mocks import statement, and disable ImportError if a module
    could not be imported.
    :param packages: a list of prefixes of modules that should
        be mocked, and an ImportError could not be raised for.
    :param mock_kwargs: kwargs for MagicMock object.
    :return: patch object
    """

    def try_import(module_name, *args, **kwargs):
        try:
            return _builtins_import(module_name, *args, **kwargs)
        except:
            if any((module_name == prefix or module_name.startswith(prefix + '.') for prefix in packages)):
                return mock.MagicMock(**mock_kwargs)
            raise

    return mock.patch('six.moves.builtins.__import__', try_import)
