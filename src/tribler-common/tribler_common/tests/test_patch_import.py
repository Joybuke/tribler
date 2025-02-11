from unittest.mock import MagicMock

import pytest

from tribler_common.patch_import import patch_import

pytestmark = pytest.mark.asyncio


# pylint: disable=import-outside-toplevel, import-error, unused-import
# fmt: off

@patch_import(['library_that_does_not_exist'])
async def test_mock_import_mocked_lib():
    import library_that_does_not_exist
    assert library_that_does_not_exist

    # test that mocks for inner inner function are presented
    assert library_that_does_not_exist.inner_function

    # test that magic methods of objects from patched library works correctly
    assert len(library_that_does_not_exist.inner_set) == 0


@patch_import([])
async def test_mock_import_import_real_lib():
    with pytest.raises(ImportError):
        import library_that_does_not_exist
        # `library_that_does_not_exist.inner_function()` call is unnecessary for the test itself, but it prevents
        # removing "unused" `import library_that_does_not_exist` during IDE autoformat procedure.
        library_that_does_not_exist.inner_function()


@patch_import(['time'])
async def test_mock_import_not_strict():
    import time
    assert not isinstance(time, MagicMock)


@patch_import(['time'], strict=True)
async def test_mock_import_strict():
    import time
    assert isinstance(time, MagicMock)


@patch_import(['time'], always_raise_exception_on_import=True)
async def test_mock_import_always_raise_exception_on_import():
    with pytest.raises(ImportError):
        import time
        # `time.gmtime(0)` call is unnecessary for the test itself, but it prevents removing "unused"
        # `import time` during IDE autoformat procedure.
        time.gmtime(0)
