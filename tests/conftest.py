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
    with unittest.mock.patch("sys.stdin", StringIO("!!")):
        yield


@pytest.fixture
def mock_p():
    """Mock and yield a 'P' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('P')):
        yield


@pytest.fixture
def mock_c():
    """Mock and yield a 'C' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('C')):
        yield


@pytest.fixture
def mock_m():
    """Mock and yield a 'M' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('M')):
        yield


@pytest.fixture
def mock_n():
    """Mock and yield a 'N' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('N')):
        yield


@pytest.fixture
def mock_d():
    """Mock and yield a 'D' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('D')):
        yield


@pytest.fixture
def mock_r():
    """Mock and yield a 'R' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('R')):
        yield


@pytest.fixture
def mock_1():
    """Mock and yield a '1' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('1')):
        yield

@pytest.fixture
def mock_4():
    """Mock and yield a '4' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('4')):
        yield


@pytest.fixture
def mock_5():
    """Mock and yield a '5' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('5')):
        yield


@pytest.fixture
def mock_7():
    """Mock and yield a '7' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('7')):
        yield


@pytest.fixture
def mock_11():
    """Mock and yield a '11' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('11')):
        yield


@pytest.fixture
def mock_p3_s1():
    """Mock and yield two P and one 1 input entries for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('P\nP\n1\n')):
        yield


@pytest.fixture
def mock_exc():
    """Mock and yield '!!' input entry for AxeProfiler."""
    with unittest.mock.patch("sys.stdin", StringIO('!!')):
        yield
