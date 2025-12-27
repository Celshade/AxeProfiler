import os
import json

from temp_config import TempConfig
from axeprofiler.cli import Cli


# NOTE `tmp_path` is a pytest built-in that creates a per-test tmp dir
# breaks in a class for some reason - returns a list instead of str path
def test_no_profiles(tmp_path, capsys):
    with TempConfig(str(tmp_path.joinpath())) as temp:
        assert os.path.exists(".config")
        assert os.path.exists(".config.backup")
        with open(".config", 'r') as f:
            print(json.loads(f.read()), end='\n')

        cli = Cli()
        assert cli.num_profiles == 0
        # cli.list_profiles(first_page=True)
        # print(capsys.readouterr())
        # assert 0


# def test_list_one_page():
#     raise NotImplementedError


# def test_list_mul_page():
#     raise NotImplementedError
