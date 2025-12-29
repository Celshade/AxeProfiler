import os
import json

from shared import TempConfig
from axeprofiler.cli import Cli


# TODO breakout core test logic into a function with strong param flexibility
#  set args and call from within each test_func() to consolidate

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


def test_list_mul_page_q(tmp_path, mock_q, capsys):
    path = str(tmp_path.joinpath()) + '/'
    # print(path)  # NOTE testing
    with TempConfig(path, 6):
        # print(os.listdir(path))  # NOTE testing
        # Test for more than 1 page (4 per page)
        cli = Cli()
        assert cli.profile_dir == path
        assert cli.num_profiles == 6
        cli.list_profiles(first_page=True)

        # Test for [P] (page) option
        out = str(capsys.readouterr())
        # print(out)  # NOTE testing
        assert "[P]" in out
        # assert 0  # NOTE testing


def test_list_mul_page_7(tmp_path, mock_7, capsys):
    path = str(tmp_path.joinpath()) + '/'
    # print(path)  # NOTE testing
    with TempConfig(path, 7):
        # print(os.listdir(path))  # NOTE testing
        # Test for more than 1 page (4 per page)
        cli = Cli()
        assert cli.profile_dir == path
        assert cli.num_profiles == 7
        cli.list_profiles(profiles=os.listdir(cli.profile_dir)[4:],
                          num_rendered=4)

        # Test for [P] (page) option removed due to prompt clear on final page
        out = str(capsys.readouterr())
        print(out)  # NOTE testing
        assert "[P]" not in out
        # assert 0  # NOTE testing


def test_list_mul_page_select_forward(tmp_path, mock_7, capsys):
    path = str(tmp_path.joinpath()) + '/'
    # print(path)  # NOTE testing
    with TempConfig(path, 7):
        # print(os.listdir(path))  # NOTE testing
        # Test for more than 1 page (4 per page)
        cli = Cli()
        assert cli.profile_dir == path
        assert cli.num_profiles == 7
        cli.list_profiles(first_page=True)

        # Test for [P] (page) option and 7 in choices (which is mocked input)
        out = str(capsys.readouterr())
        # print(out)  # NOTE testing
        assert all(("[P]" in out, '7' in out))
        # assert 0  # NOTE testing


def test_list_mul_page_select_retro(tmp_path, mock_1, capsys):
    path = str(tmp_path.joinpath()) + '/'
    # print(path)  # NOTE testing
    with TempConfig(path, 5):
        # print(os.listdir(path))  # NOTE testing
        # Test for more than 1 page (4 per page)
        cli = Cli()
        assert cli.profile_dir == path
        assert cli.num_profiles == 5
        cli.list_profiles(profiles=os.listdir(cli.profile_dir)[4:],
                          num_rendered=4)

        # Test successful pagination and retro selection
        out = str(capsys.readouterr())
        print(out)  # NOTE testing
        assert "[P]" not in out

        assert cli.profile
        assert cli.profile.name == os.listdir(cli.profile_dir)[0].split('.')[0]
        # assert 0  # NOTE testing
