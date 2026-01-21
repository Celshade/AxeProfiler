import os
import unittest.mock
from io import StringIO

from shared import TempConfig
from axeprofiler.cli import Cli


def test_run_profile_cancel(tmp_path):
    path = f"{tmp_path.joinpath()}/"
    with TempConfig(path, num_profiles=1):
        cli = Cli()
        filename = os.listdir(path)[0]
        profile = cli._load_profile(filename)
        called = False

        def fake_run(ip):
            nonlocal called
            called = True

        profile.run_profile = fake_run
        # ensure cli.profile is set since Cli.run_profile uses self.profile
        cli.profile = profile

        # Mock network info response and provide IP then 'n' to cancel
        def fake_request(ip, endpoint, body=None):
            class R:
                def json(self_inner):
                    return {'hostname': 'active', 'frequency': 600,
                            'coreVoltage': 1200, 'fanspeed': 100}
            return R()

        with unittest.mock.patch('axeprofiler.profiles.request',
                                 side_effect=fake_request):
            with unittest.mock.patch('sys.stdin', StringIO('1.2.3.4\nn\n')):
                cli.run_profile(profile)

        assert not called


def test_run_profile_apply_calls_run(tmp_path):
    path = f"{tmp_path.joinpath()}/"
    with TempConfig(path, num_profiles=1):
        cli = Cli()
        filename = os.listdir(path)[0]
        profile = cli._load_profile(filename)
        called = []

        def fake_run(ip):
            called.append(ip)

        profile.run_profile = fake_run
        # ensure cli.profile is set since Cli.run_profile uses self.profile
        cli.profile = profile

        def fake_request(ip, endpoint, body=None):
            class R:
                def json(self_inner):
                    return {'hostname': 'active', 'frequency': 600,
                            'coreVoltage': 1200, 'fanspeed': 100}
            return R()

        with unittest.mock.patch('axeprofiler.profiles.request',
                                 side_effect=fake_request):
            with unittest.mock.patch('sys.stdin', StringIO('1.2.3.4\ny\n')):
                cli.run_profile(profile)

        assert called == ['1.2.3.4']
