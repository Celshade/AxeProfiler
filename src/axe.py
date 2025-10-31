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
from os import system

from rich.panel import Panel
from rich.prompt import Confirm
from rich import print as rprint

from cli import Cli
from api import request


def show_notice() -> bool:
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
        return Confirm.ask("Do you want to start the program?", default='y')
    except FileNotFoundError:
        msg = ''.join(("Could not render the [red]copyright[/] notice.\n",
                        "Please see line 4 of any source file or ",
                        f"[red]{copying}[/] for more details."))
        rprint(Panel(msg, title="[bold bright_cyan]Copyright Notice",
                        width=80))
        return Confirm.ask("Do you want to start the program?", default='y')


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
    start = show_notice()
    if start:
        cli = Cli()
        cli.session()
