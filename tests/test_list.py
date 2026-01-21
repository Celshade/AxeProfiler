import os
import json
import unittest
from io import StringIO

from shared import TempConfig
from axeprofiler.cli import Cli


# NOTE `tmp_path` == pytest Fixture that creates a per-test temp dir
def test_config_handling(tmp_path: str):
    path = f"{tmp_path.joinpath()}/"
    with TempConfig(path):
        # Validate config setup and backup
        assert os.path.exists(".config")
        assert os.path.exists(".config.backup")

        # Validate path contents within config
        with open(".config", 'r') as f:
            assert json.loads(f.read()).get("profile_dir") == path
            # print(json.loads(f.read()), end='\n')

    # Validate temp config tare-down and backup reinstated.
    assert os.path.exists(".config")
    assert not os.path.exists(".config.backup")


def create_cli_and_test_list(
        path: str,
        stdout: str | None = None,
        num_profiles: int | None = 0,
        first_page: bool = True,
        profiles: tuple[int | None] = None,
        num_rendered: int = 0,
        message_in: list[str] | None = [],
        message_out: list[str] | None = [],
        return_cli: bool = False,
        extra_profile: dict | None = None
):
    with TempConfig(path, num_profiles=num_profiles,
                    extra_profile=extra_profile):
        cli = Cli()  # init CLI
        assert cli.profile_dir == path  # Validate path

        # Handle page listing
        if profiles:
            lower_bound, upper_bound = profiles
            cli.list_profiles(profiles=os.listdir(path)[lower_bound:upper_bound],
                              num_rendered=num_rendered, first_page=first_page)
        else:
            cli.list_profiles(num_rendered=num_rendered, first_page=first_page)

        # Validate output
        if (message_in or message_out) and stdout:
            output = str(stdout.readouterr())
            # print(output)

            # Validate custom output
            for substring in message_in:
                assert substring in output

            for substring in message_out:
                assert substring not in output

        # Optionally return the instantiated Cli for further assertions
        if return_cli:
            return cli


def test_no_profiles(tmp_path, mock_q, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, stdout=capsys, num_profiles=0,
                             message_in=["(Q)"])


def test_list_one_page(tmp_path, mock_q, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, stdout=capsys, num_profiles=1,
                             message_in=["(Q)"])


def test_list_mul_page_q(tmp_path, mock_q, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, stdout=capsys, num_profiles=6,
                             message_in=["1-4/6", "[1...6]", "(P)"],
                             message_out=["(Q)"])


def test_list_mul_page_select_forward(tmp_path, mock_7, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, num_profiles=7,
                             message_in=["1-4/7", "[1...7]", "(P)"])


def test_list_mul_page_select_retro(tmp_path, mock_1, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(
        path=path, stdout=capsys, num_profiles=5, first_page=False,
        profiles=(4, 5), num_rendered=4,
        message_in=["5-5/5", "[1...5]", "(Q)"], message_out=["(P)"]
    )


def test_list_mul_page_2(tmp_path, mock_5, capsys):
    path = f"{tmp_path.joinpath()}/"

    create_cli_and_test_list(
        path=path, stdout=capsys, num_profiles=5, first_page=False,
        profiles=(4, 5), num_rendered=4,
        message_in=["5-5/5", "[1...5]", "(Q)"], message_out=["(P)"]
    )


def test_select_profile_sets_cli_profile(tmp_path, mock_1):
    path = f"{tmp_path.joinpath()}/"
    cli = create_cli_and_test_list(path=path, num_profiles=3, return_cli=True)

    assert cli
    assert cli.profile
    assert cli.profile.name == 'test_0'


def test_render_profile_contents(tmp_path, mock_q, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, stdout=capsys, num_profiles=1,
                             message_in=['test_0', 'frequency'])


def test_get_page_count_second_page_range(tmp_path, mock_q, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, stdout=capsys, num_profiles=8,
                             num_rendered=4, first_page=False,
                             message_in=['5-8/8'])


def test_multi_step_pagination_and_select(tmp_path, mock_p3_s1):
    path = f"{tmp_path.joinpath()}/"
    # create 9 profiles to require 3 pages
    cli = create_cli_and_test_list(path=path, num_profiles=9, return_cli=True)

    assert cli
    assert cli.profile


def test_load_profile_file_not_found(tmp_path, mock_q, capsys):
    path = f"{tmp_path.joinpath()}/"
    cli = create_cli_and_test_list(path=path, num_profiles=0, return_cli=True)
    # Request a non-existent file
    res = cli._load_profile('nope.json')
    out = capsys.readouterr().out

    assert not res
    assert 'Could not find a profile named' in out


def test_truncation_long_profile_name(tmp_path, mock_q, capsys):
    path = f"{tmp_path.joinpath()}/"
    long_name = 'a' * 80
    # Provide the long-name profile via the helper's extra_profile dict
    extra_profile = {
        'profile_name': long_name,
        'hostname': 'Unknown',
        'frequency': 600,
        'coreVoltage': 1200,
        'fanspeed': 100
    }

    # Use the helper to create the profile and return the Cli
    cli = create_cli_and_test_list(path=path, num_profiles=0,
                                   extra_profile=extra_profile,
                                   return_cli=True)

    # Re-run the listing while capturing output to inspect truncation
    with unittest.mock.patch("sys.stdin", StringIO('Q')):
        cli.list_profiles(first_page=True)

    output = capsys.readouterr().out
    # Filter out setup/creation messages
    filtered = '\n'.join(
        line for line in output.splitlines()
        if 'profile created at:' not in line
        and 'extra profile created at:' not in line
    )
    # Full long name should not be printed in the listing
    assert long_name not in filtered
    assert '…' in filtered or '...' in filtered
