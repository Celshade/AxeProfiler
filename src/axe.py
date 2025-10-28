# AxeProfiler is a program designed to make saving/switching configurations for
# bitcoin miner devices simpler and more efficient.

# Copyright (C) 2025 [DC] Celshade <ggcelshade@gmail.com>

# This file is part of AxeProfiler.

# AxeProfiler is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# AxeProfiler is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# AxeProfiler. If not, see <https://www.gnu.org/licenses/>.

# from time import sleep  # TODO remove after testing
import json
from time import sleep
from os import system, path, mkdir, listdir

from rich.panel import Panel
from rich import print as rprint

from cli import Cli
from api import request
from profiles import Profile


def show_notice() -> None:
    try:
        root = __file__.split('src')[0]
        notice = f"{root}.notice"
        copying = f"{root}COPYING"

        with open(notice, 'r') as f:
            notice = f.read()

        system("clear")  # NOTE @Linux; handle MAC/Windows
        rprint(Panel(f"{notice}[bold magenta]{copying}.",
                     title="[bold bright_cyan]Copyright Notice",
                     width=80))
        sleep(2.2)  # Let the user at least skim over the notice
    except FileNotFoundError:
        msg = ''.join(("Could not render the [red]copyright[/] notice.\n",
                        "Please see line 4 of any source file or ",
                        f"[red]{copying}[/] for more details."))
        rprint(Panel(msg, title="[bold bright_cyan]Copyright Notice",
                        width=80))
        sleep(2.2)  # Let the user at least skim over the notice


def get_current_config(ip: str) -> dict[str, str] | None:
    """Get the current config from the device at the given IP.

    Args:
        ip: The IP of the [axe] device.
    """
    # Get existing freq/c.volt
    data = request(ip, "info").json()

    if not data:
        print("Nothing returned from the request ❔")
        return None

    # pprint(data)
    profile_data = {
        key: data[key] for key in data.keys() & (
            "hostname", "frequency", "coreVoltage", "fanspeed"
        )
    }
    profile_data["IP"] = ip

    # print(profile_data)  # TODO remove
    return profile_data


# def check_for_profiles() -> None:
#     """Check for an existing `profiles` dir and create one if needed.
#     """
#     try:
#         if not path.isdir("./.profiles"):
#             mkdir("./.profiles")
#             assert path.exists("./.profiles")
#             print("No profiles dir - creating local profiles dir at . ✅")
#         elif num_profiles := len(listdir("./.profiles")):
#             # TODO enhance verification?
#             print(f"{num_profiles} existing files found! ✅")
#         else:
#             print("`Profiles` dir exists, but no profiles found 📂")
#     except AssertionError:
#         print("Failed to create a `profiles` dir 😢")


def create_profile(config: dict[str, str],
                   profile_name: str | None = None) -> Profile | None:
    """Create and save a profile for the given config.

    Args:
        config: The config data to save to the profile.
        profile_name(optional): The profile name (default=None).
    Returns:
        A `Profile` obj containing axe config data.
    """
    try:
        # check_for_profiles()
        profile = Profile.create_profile(
            {
                "profile_name": profile_name or
                    input("Enter a name for this profile: ") or
                    "default",
                **config
            }
        )
        profile.save_profile()
        assert path.exists(f"./.profiles/{profile.name}.json")

        print(f"Profile: {profile.name} created! ✅")
        return profile
    except AssertionError:
        print("Error verifying profile was saved")
    except Exception as e:
        raise e


def load_profile(profile_name: str) -> Profile:
    """Load an existing profile.

    Args:
        profile_name: The name of the profile to load.
    Returns:
        A `Profile` obj containing axe config data.
    Raises:
        FileNotFoundError: if no file is found for the given name.
    """
    try:
        print("Loading profile... ⏳")
        with open(f"./.profiles/{profile_name}.json", 'r') as f:
            return Profile.create_profile(json.loads(f.read()))

    except FileNotFoundError:
        print(f"Could not find a profile named: {profile_name} ⚠")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # TODO remove testing
    # # device_ip = "192.168.0.2"  # input("Enter IP: ")  # NOTE g1
    # device_ip = "192.168.0.7"  # input("Enter IP: ")  # NOTE s0
    # config = get_current_config(ip=device_ip)
    # # create profile
    # profile = create_profile(config=config)
    # print()
    # print(profile)
    # print()

    # # compare active profile vs saved profile
    # existing_profile = load_profile(profile.name)
    # if profile.data != existing_profile.data:
    #     print("Profile does not match before and after saving")
    #     print(existing_profile.data)

    # # check repr of profile
    # print(profile.__repr__())
    # print()

    # # update profile
    # # TODO confirm if update (PATCH API) also resets by default?? seems to
    # profile.update_profile(
    #     # {"frequency": 500, "coreVoltage": 1125, "fanspeed": 69}  # NOTE: g1
    #     {"frequency": 750, "coreVoltage": 1250, "fanspeed": 99}  # NOTE: s0
    # )

    # # test profile name change (filename)
    # print()
    # profile.update_profile({"profile_name": "test2.CHANGED3"})

    # # push updated configs to device and restart
    # # profile.run_profile(ip="192.168.0.2", update=True)  # NOTE g1
    # profile.run_profile(ip="192.168.0.7", update=True)  # NOTE s0

    # # Check new config
    # sleep(5)
    # config = get_current_config(ip=device_ip)
    # # create profile
    # print("Reloading saved profile to verify data... ⏳")
    # profile = create_profile(config=config, profile_name=profile.name)
    # print(profile.data)
    # # TODO add await handling or give time between API calls

    # Run the CLI
    show_notice()
    cli = Cli()
    cli.session()
