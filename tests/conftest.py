"""
A module of pytest fixtures that mock AxeProfiler user input
"""
import unittest.mock
from io import StringIO

import pytest


@pytest.fixture
def mock_q():
    """Mock and yield a 'Q' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('Q')):
        yield


@pytest.fixture
def mock_exclaim():
    """Mock and yield a '!!' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('Q')):
        yield


@pytest.fixture
def mock_p():
    """Mock and yield a 'P' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('Q')):
        yield


@pytest.fixture
def mock_c():
    """Mock and yield a 'C' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('Q')):
        yield


@pytest.fixture
def mock_m():
    """Mock and yield a 'M' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('Q')):
        yield


@pytest.fixture
def mock_n():
    """Mock and yield a 'N' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('Q')):
        yield


@pytest.fixture
def mock_d():
    """Mock and yield a 'D' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('Q')):
        yield


@pytest.fixture
def mock_r():
    """Mock and yield a 'R' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('Q')):
        yield

