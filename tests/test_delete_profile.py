import os

from shared import TempConfig
from axeprofiler.cli import Cli


def test_delete_profile_confirm(tmp_path, mock_y):
    path = f"{tmp_path.joinpath()}/"
    with TempConfig(path, num_profiles=1):
        cli = Cli()
        # load created profile file
        filename = os.listdir(path)[0]
        profile = cli._load_profile(filename)

        assert os.path.exists(f"{path}{profile.name}.json")
        # confirm deletion via mock_y
        cli.delete_profile(profile)
        # file should be removed and cli.profile cleared
        assert not os.path.exists(f"{path}{profile.name}.json")
        assert not cli.profile


def test_delete_profile_cancel(tmp_path, mock_n):
    path = f"{tmp_path.joinpath()}/"
    with TempConfig(path, num_profiles=1):
        cli = Cli()
        filename = os.listdir(path)[0]
        profile = cli._load_profile(filename)
        cli.profile = profile  # select profile

        assert os.path.exists(f"{path}{profile.name}.json")
        # cancel deletion via mock_n
        cli.delete_profile(profile)
        # file should still exist and profile should remain selected
        assert os.path.exists(f"{path}{profile.name}.json")
        assert cli.profile
