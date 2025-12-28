import os
import json

from utils import TempConfig
from axeprofiler.cli import Cli


# NOTE `tmp_path` is a pytest built-in that creates a per-test tmp dir
#   breaks in a class for some reason - returns a list instead of str path
def test_no_profiles(tmp_path, mock_q, capsys):
    path = str(tmp_path.joinpath()) + '/'
    with TempConfig(path):
        # TODO break these config file asserts into their own test
        assert os.path.exists(".config")
        assert os.path.exists(".config.backup")
        with open(".config", 'r') as f:
            assert json.loads(f.read()).get("profile_dir") == path
            # print(json.loads(f.read()), end='\n')

        # Test for 0 profiles
        cli = Cli()
        assert cli.num_profiles == 0
        cli.list_profiles(first_page=True)

        # Test for no [P] (page) option
        out = str(capsys.readouterr())
        assert "[P]" not in out


def test_list_one_page(tmp_path, mock_q, capsys):
    path = str(tmp_path.joinpath()) + '/'
    # print(path)  # NOTE testing
    with TempConfig(path, 1):
        # print(os.listdir(path))  # NOTE testing
        # Test for 1 profiles
        cli = Cli()
        assert cli.profile_dir == path
        assert cli.num_profiles == 1
        cli.list_profiles(first_page=True)

        # Test for no [P] (page) option
        out = str(capsys.readouterr())
        assert "[P]" not in out
        # assert 0  # NOTE testing


def test_list_mul_page(tmp_path, mock_q, capsys):
    path = str(tmp_path.joinpath()) + '/'
    # print(path)  # NOTE testing
    with TempConfig(path, 5):
        # print(os.listdir(path))  # NOTE testing
        # Test for more than 1 page (4 per page)
        cli = Cli()
        assert cli.profile_dir == path
        assert cli.num_profiles > 4
        cli.list_profiles(first_page=True)

        # Test for [P] (page) option
        out = str(capsys.readouterr())
        # print(out)  # NOTE testing
        assert "[P]" in out
        # assert 0  # NOTE testing
