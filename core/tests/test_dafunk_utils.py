#!/usr/bin/env python

"""Tests for `dafunk_core_library` package."""

import pytest  # noqa: F401
import os
from core.dafunk.utils import tar_file

actual_path = os.path.dirname(os.path.abspath(__file__))


def test_compress_folder():
    tar_file("dafunk_test_command.tar.gz", os.path.join(actual_path, 'files', "dafunk_test_command"))
