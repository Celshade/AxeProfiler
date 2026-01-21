import os

from shared import TempConfig
from axeprofiler.cli import Cli


def test_show_profile_no_selection(tmp_path, capsys):
    path = f"{tmp_path.joinpath()}/"
    with TempConfig(path):
        cli = Cli()
        res = cli.show_profile(None)

        assert "No Profile is currently selected" in capsys.readouterr().out
        assert not res


def test_show_profile_display_and_confirm(tmp_path, mock_y):
    path = f"{tmp_path.joinpath()}/"
    with TempConfig(path, num_profiles=1):
        cli = Cli()
        # load the created profile file (test_0.json)
        profile = cli._load_profile(os.listdir(path)[0])
        assert profile

        # Ask confirm via show_profile
        res = cli.show_profile(profile, message="Confirm?", choices=['y','n'],
                               show_choices=True, show_default=True,
                               default=True, prompt=False)
        assert res
