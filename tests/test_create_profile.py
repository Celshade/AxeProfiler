import os
from io import StringIO
import unittest.mock

from shared import TempConfig
from axeprofiler.cli import Cli


def test_create_profile_success(tmp_path, create_default):
    path = f"{tmp_path.joinpath()}/"
    with TempConfig(path):
        cli = Cli()
        profile = cli.create_profile()
        # ensure profile object returned and file exists
        assert profile
        assert os.path.exists(f"{path}{profile.name}.json")


def test_create_profile_cancel(tmp_path, mock_exclaim):
    path = f"{tmp_path.joinpath()}/"
    # First input is '!!' to cancel during _get_profile_config (mock_exc)
    with TempConfig(path):
        cli = Cli()
        profile = cli.create_profile()
        # creation cancelled, should return None and no files created
        assert not profile
        # directory should be empty
        assert len(os.listdir(path)) == 0
