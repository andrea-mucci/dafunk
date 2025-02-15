import pytest

from builder.routes import build


def test_build_route():
    build()
    assert True == False

