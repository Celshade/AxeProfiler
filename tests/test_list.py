import os
import json

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
        profiles: list[str] = None,
        num_rendered: int = 0,
        message_in: list[str] | None = [],
        message_out: list[str] | None = []
):
    with TempConfig(path, num_profiles=num_profiles):
        cli = Cli()  # init CLI
        assert cli.profile_dir == path  # Validate path
        assert cli.num_profiles == num_profiles  # Validate profile count

        # Handle page listing
        cli.list_profiles(profiles=profiles, num_rendered=num_rendered,
                          first_page=first_page)

        # Validate output
        if (message_in or message_out) and stdout:
            output = str(stdout.readouterr())
            print(output)

            for substring in message_in:
                assert substring in output

            for substring in message_out:
                assert substring not in output


def test_no_profiles(tmp_path, mock_q, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, stdout=capsys,
                             num_profiles=0, message_out=["[P]"])


def test_list_one_page(tmp_path, mock_q, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, stdout=capsys,
                             num_profiles=1, message_out=["[P]"])


def test_list_mul_page_q(tmp_path, mock_q, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, stdout=capsys,
                             num_profiles=6, message_in=["[P]"])


# FIXME x-y count is off on the upper end (tests-only)
# FIXME [P] showing in output where it shouldnt
def test_list_mul_page_7(tmp_path, mock_7, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, stdout=capsys,
                             num_profiles=7, first_page=False,
                             profiles=os.listdir(path)[4:],
                             num_rendered=4, message_out=["[P]"])


def test_list_mul_page_select_forward(tmp_path, mock_7, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, num_profiles=7, message_in=["[P]", '7'])

    # Test for [P] (page) option and 7 in choices (which is mocked input)


# def test_list_mul_page_select_retro(tmp_path, mock_1, capsys):
#     path = f"{tmp_path.joinpath()}/"
#     # print(path)  # NOTE testing
#     with TempConfig(path, 5):
#         # print(os.listdir(path))  # NOTE testing
#         # Test for more than 1 page (4 per page)
#         cli = Cli()
#         assert cli.profile_dir == path
#         assert cli.num_profiles == 5
#         cli.list_profiles(profiles=os.listdir(cli.profile_dir)[4:],
#                           num_rendered=4)

#         # Test successful pagination and retro selection
#         out = str(capsys.readouterr())
#         print(out)  # NOTE testing
#         assert "[P]" not in out

#         assert cli.profile
#         assert cli.profile.name == os.listdir(cli.profile_dir)[0].split('.')[0]
#         # assert 0  # NOTE testing
