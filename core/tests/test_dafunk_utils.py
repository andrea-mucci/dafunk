#!/usr/bin/env python

"""Tests for `dafunk_core_library` package."""
import shutil

import pytest  # noqa: F401
import os
from core.dafunk.utils import tar_file, untar_file

actual_path = os.path.dirname(os.path.abspath(__file__))


def test_compress_folder():
    tar_file("dafunk_test_command.tar.gz", os.path.join(actual_path, 'files', "dafunk_test_command"))
    assert os.path.exists(os.path.join(actual_path, "dafunk_test_command.tar.gz")) == True
    os.remove(os.path.join(actual_path, "dafunk_test_command.tar.gz"))

def test_uncompress_folder():
    tar_file("dafunk_test_command.tar.gz", os.path.join(actual_path, 'files', "dafunk_test_command"))
    assert os.path.exists(os.path.join(actual_path, "dafunk_test_command.tar.gz")) == True
    untar_file(os.path.join(actual_path, "dafunk_test_command.tar.gz"))
    assert os.path.isdir(os.path.join(actual_path, "dafunk_test_command")) == True
    assert os.path.exists(os.path.join(actual_path, "dafunk_test_command", ".gitignore")) == True
    assert os.path.exists(os.path.join(actual_path, "dafunk_test_command", "main.py")) == True
    os.remove(os.path.join(actual_path, "dafunk_test_command.tar.gz"))
    shutil.rmtree(os.path.join(actual_path, "dafunk_test_command"))
