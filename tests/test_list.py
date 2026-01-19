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
        profiles: tuple[int | None] = None,
        num_rendered: int = 0,
        message_in: list[str] | None = [],
        message_out: list[str] | None = []
):
    with TempConfig(path, num_profiles=num_profiles):
        cli = Cli()  # init CLI
        assert cli.profile_dir == path  # Validate path
        assert cli.num_profiles == num_profiles  # Validate profile count

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


def test_list_mul_page_2(tmp_path, mock_5, capsys):
    path = f"{tmp_path.joinpath()}/"

    create_cli_and_test_list(
        path=path, stdout=capsys, num_profiles=5, first_page=False,
        profiles=(4, 5), num_rendered=4,
        message_in=["5-5/5", "[1...5]", "(Q)"], message_out=["(P)"]
    )


def test_list_mul_page_select_forward(tmp_path, mock_7, capsys):
    path = f"{tmp_path.joinpath()}/"
    create_cli_and_test_list(path=path, num_profiles=7,
                             message_in=["1-4/7", "[1...7]", "(P)"])


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
