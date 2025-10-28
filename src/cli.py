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

import json
from math import ceil
from time import sleep
from time import sleep
from typing import TypeAlias
from os import system, path, mkdir, listdir

from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.columns import Columns
from rich.console import Console, Group
from rich.progress import Progress

from profiles import Profile


CONFIG: TypeAlias = dict[str, str | int]  # config obj format


class Cli(Console):
    def __init__(self) -> None:
        super().__init__()  # Inherit Console() ability to render/color
        self.__root: str  = __file__.split("src")[0]  # program root
        self.__config: str  = f"{self.__root}.config"  # program config

        # Start progress bar
        with Progress() as progress:
            # Check for existing config or create one
            config_task = progress.add_task("[blue]Validating config files...")
            progress.update(config_task, advance=25)
            if not path.exists(self.__config):
                with open(self.__config, 'w') as f:
                    f.write(json.dumps(
                        {"profile_dir": f"{self.__root}.profiles/"},
                        indent=4))

            # Read config
            progress.update(config_task, advance=50)
            with open(self.__config, 'r') as f:
                config = json.loads(f.read())
            progress.update(config_task, advance=25)

            profile_task = progress.add_task("[blue]Validating profiles...")
            try:
                # Verify integrity of profile_dir
                profile_dir = config.get("profile_dir")
                progress.update(profile_task, advance=30)
                if not profile_dir:
                    # Add default profile_dir to config
                    with open(self.__config, 'w') as f:
                        config["profile_dir"] = f"{self.__root}.profiles/"
                        f.write(json.dumps(config, indent=4))

                    # Make default profile_dir and assign class attr
                    mkdir(self.__profile_dir)
                    self.__profile_dir = config["profile_dir"]
                else:
                    assert profile_dir
                    assert isinstance(profile_dir, str)

                    # Ensure existing profile_dir
                    if not path.exists(profile_dir):
                        mkdir(profile_dir)

                    self.__profile_dir = profile_dir  # assign class attr
                progress.update(profile_task, advance=70)
            except AssertionError:
                msg = "[red]Invalid profile directory configuration"
                self.print(msg)
                raise AssertionError("**Program terminated**")  # Exit program

        self.print("[blue]Starting program...")
        sleep(1)  # Pause render before clearing

    def __repr__(self):
        return f"Cli()"

    @property
    def profile_dir(self) -> str:
        return self.__profile_dir

    @property
    def num_profiles(self) -> int | None:
        return len(listdir(self.profile_dir))


    def main_menu(self) -> None:
        system("clear")  # NOTE @Linux; handle MAC/Windows

        # Create the main menu as a table
        menu = Table("Option", "Description",
                     title="[green]Enter one of the following options",
                     width=76)

        # Add a row for each menu option
        menu.add_row(f"[bold green]L [white]({self.num_profiles} found)",
                     "List all of the available Profiles")
        menu.add_row("[bold green]N", "Create a new Profile")
        menu.add_row("[bold green]U", "Update an existing Profile")
        menu.add_row("[bold green]R", "Run an existing Profile")
        menu.add_row("[bold green]D", "Delete an existing Profile")
        menu.add_row(
            "[bold bright_cyan]M [white](default)", "Show this menu again")
        menu.add_row("[bold red]Q", "Quit the program")

        # Render the main menu
        self.print(Panel(menu, title="[bold bright_cyan]Main Menu", width=80))

    def load_profile(self, profile_name: str) -> Profile:
        """Load an existing profile.

        Args:
            profile_name: The name of the profile to load.
        Returns:
            A `Profile` obj containing axe config data.
        Raises:
            FileNotFoundError: if no file is found for the given name.
        """
        try:
            with open(f"{self.profile_dir}{profile_name}", 'r') as f:
                return Profile.create_profile(json.loads(f.read()))

        except FileNotFoundError:
            self.print(f"[red]Could not find a profile named: {profile_name} ⚠")
        except Exception as e:
            print(e)

    def list_profiles(self) -> None:
        """List all existing profiles.
        """
        # pages = ceil(self.num_profiles / 10)  # NOTE only if total > screen
        # TODO find out how many profiles (tables) fit inside 80 width window
          # TODO paginate based on this (assign vertical depth?)

        # NOTE renders profiles as tables; columns allow for side by side tables
        # print(self.profile_dir)
        self.print("[blue]Loading profiles... ⏳")
        profile_names = listdir(self.profile_dir)
        self.print(f"profiles: {profile_names}")  # [TESTING] TODO remove

        test = self.load_profile(profile_names[0])
        test = Table(test.__str__(), title=test.name, width=30)
        test2 = self.load_profile(profile_names[1])
        test2 = Table(test2.__str__(), title=test2.name, width=30)
        render_profiles = Panel(Columns((test, test2)),
                                title="All Tables",
                                width=80)
        self.print(render_profiles)
        user_choice = Prompt.ask("Enter [Q] to quit [italics]not case sensitive",
                                 choices=['Q'],
                                 default='Q')
        if user_choice.lower() == 'q':
            return

        # NOTE use Group in combo with Columns to create rows of profile tables

        # TODO load profiles as objects and render data

    def session(self) -> None:
        # Handle user choice
        self.main_menu()
        user_choice = Prompt.ask(
            "Enter an option ([italics]not case sensitive[/]): ",
            choices=['L', 'N', 'U', 'R', 'D', 'M', 'Q'],
            default='M',
            case_sensitive=False)

        # Run session loop via recursion
        match user_choice.lower():
            case 'l':
                # TODO List existing profiles (L)
                # # TODO separate/check by axe type (single-chip, multi-chip)
                self.print(f"[green][{user_choice}][/] >>> Listing profiles")
                sleep(0.3)
                self.list_profiles()
                self.session()
            case 'n':
                # TODO new profile (n)
                self.print(f"[green][{user_choice}][/] >>> Creating profile")
                sleep(0.3)
                self.session()
            case 'u':
                # TODO update profile (u)
                self.print(f"[green][{user_choice}][/] >>> Updating profile")
                sleep(0.3)
                self.session()
            case 'r':
                # TODO run profile (r)
                # # NOTE apply to multiple devices?
                self.print(f"[green][{user_choice}][/] >>> Running profile")
                sleep(0.3)
                self.session()
            case 'd':
                # TODO delete profile (d)
                self.print(f"[green][{user_choice}][/] >>> Deleting profile")
                sleep(0.3)
                self.session()
            case 'm':
                self.print(
                    f"[bright_cyan][{user_choice}][/] >>> Returning to menu")
                sleep(0.3)
                self.session()
            case 'q':
                self.print(f"[red][{user_choice}][/] >>> Session Terminated")
                return


if __name__ == "__main__":
    # print(__file__.split("src")[0])
    cli = Cli()
    cli.session()
