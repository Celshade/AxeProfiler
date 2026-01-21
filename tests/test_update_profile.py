import os
import unittest.mock
from io import StringIO

from shared import TempConfig
from axeprofiler.cli import Cli


def test_update_profile_keep_name_confirm(tmp_path):
    path = f"{tmp_path.joinpath()}/"
    # inputs: accept defaults for all prompts then 'y' to confirm update
    inputs = "\n\n\n\n\n y\n"

    with TempConfig(path, num_profiles=1):
        with unittest.mock.patch("sys.stdin", StringIO(inputs)):
            cli = Cli()
            filename = os.listdir(path)[0]
            profile = cli._load_profile(filename)
            assert profile

            cli.profile = profile  # set profile
            cli.update_profile(profile)
            # profile file should still exist under same name
            assert os.path.exists(f"{path}{profile.name}.json")


def test_update_profile_rename_confirm(tmp_path):
    path = f"{tmp_path.joinpath()}/"
    # inputs: new name, accept other defaults, confirm 'y'
    inputs = "renamed\n\n\n\n\ny\n"

    with TempConfig(path, num_profiles=1):
        with unittest.mock.patch("sys.stdin", StringIO(inputs)):
            cli = Cli()
            filename = os.listdir(path)[0]
            profile = cli._load_profile(filename)
            cli.profile = profile  # set profile
            old_name = profile.name
            cli.update_profile(profile)

            # old file should be replaced by new file
            assert not os.path.exists(f"{path}{old_name}.json")
            assert os.path.exists(f"{path}renamed.json")


def test_update_profile_cancel(tmp_path, mock_exclaim):
    path = f"{tmp_path.joinpath()}/"
    with TempConfig(path, num_profiles=1):
        cli = Cli()
        filename = os.listdir(path)[0]
        profile = cli._load_profile(filename)
        cli.profile = profile  # set profile
        # mock_exc provides '!!' which cancels during _get_profile_config
        cli.update_profile(profile)
        # original file should remain
        assert os.path.exists(f"{path}{profile.name}.json")
