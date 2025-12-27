import os
import json

from utils import TempConfig
from axeprofiler.cli import Cli


# NOTE `tmp_path` is a pytest built-in that creates a per-test tmp dir
#   breaks in a class for some reason - returns a list instead of str path
def test_no_profiles(tmp_path, mock_q, capsys):
    with TempConfig(str(tmp_path.joinpath())) as temp:
        assert os.path.exists(".config")
        assert os.path.exists(".config.backup")
        with open(".config", 'r') as f:
            print(json.loads(f.read()), end='\n')

        cli = Cli()
        assert cli.num_profiles == 0
        cli.list_profiles(first_page=True)

        out = str(capsys.readouterr())
        assert "Enter [P]" not in out


# def test_list_one_page():
#     raise NotImplementedError


# def test_list_mul_page():
#     raise NotImplementedError
