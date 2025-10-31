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
from rich.prompt import Prompt, IntPrompt as IPrompt
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
        with Progress() as progress:  # NOTE remove increments? - loads too fast
            # Check for existing config or create one
            config_task = progress.add_task("[blue]Validating config files...")
            progress.update(config_task, advance=25)
            if not path.exists(self.__config):
                with open(self.__config, 'w') as f:
                    f.write(json.dumps(
                        {"profile_dir": f"{self.__root}.profiles/"},
                        indent=4)
                    )

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
        sleep(0.5)  # Pause render before clearing

    def __repr__(self):
        return f"Cli()"

    def __str__(self) -> str:
        # TODO implement
        return ""

    @property
    def profile_dir(self) -> str:
        return self.__profile_dir

    @property
    def num_profiles(self) -> int:
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
        menu.add_row("[bold green]R", "Run the selected Profile")
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

    def list_profiles(self, profiles: list[str] | None = None,
                      num_rendered: int = 0) -> None:
        """List all existing profiles.

        Args:
            profiles: An array of profile names.
            num_rendered: The number of profiles rendered so far (default=0).
        """
        # TODO next iteration, add filters
        self.print("[blue]Loading profiles... ⏳")

        # Turn each Profile() into a renderable Table()
        # NOTE: max 2x2 (4) per page (width=37)
        _profiles = profiles or listdir(self.profile_dir)
        # self.print(f"profiles: {_profiles}")  # [TESTING]
        tables: list[Table] = []
        for _profile in _profiles[:4]:
            profile: Profile = self.load_profile(_profile)
            # Truncate text to match profile window size with room for options
            title = Text(profile.name)
            title.truncate(max_width=32, overflow="ellipsis")
            tables.append(Table(profile.__str__(),
                                title=f"[bold magenta]{title}", width=37))

        # Get current screen totals
        if len(_profiles) >=4:
            if num_rendered == 0:
                current = "1-4"
            else:
                current = f"{num_rendered + 1}-{num_rendered + 4}"
        elif num_rendered == 0:
                current = f"1-{len(_profiles)}"
        else:
            current = f"{num_rendered + 1}-{num_rendered + len(_profiles)}"
        total = self.num_profiles  # total profiles

        # Render the profiles
        # NOTE We create rows by taking advantage of the display's built-in
        # wrapping to our set width of 80 char. This allows us to avoid
        # creating a Group() of Panel() of Columns()
        self.print(Panel(Columns(tables),
                         title=f"[bold cyan]Profiles ({current}/{total})",
                         width=80))

        # Handle user choice and menu navigation
        msg = "Enter [green][Q][/] to return to the [cyan]Main Menu[/]"
        if len(_profiles) > 4:  # Add pagination prompt
            msg += " or [green][P][/] to see more profiles"
            user_choice = Prompt.ask(msg, choices=['Q', 'P'],
                                    case_sensitive=False, default='P')
        else:
            user_choice = Prompt.ask(msg, choices=['Q'],
                                    case_sensitive=False, default='Q')

        # Use recursion to paginate as needed (4 per page)
        if user_choice.lower() == 'p' and len(_profiles) > 4:
            return self.list_profiles(profiles=_profiles[4:],
                                      num_rendered=num_rendered+4)

    def _validate_int_prompt(self, prompt: str, default: int) -> int | bool:
        """
        """
        try:
            user_choice = Prompt.ask(prompt, default=default, show_default=True)
            if isinstance(user_choice, str) and user_choice.lower() == "!!":
                return False
            return int(user_choice)

        except ValueError:
            self.print("[red]Please enter a valid integer number")
            self._validate_int_prompt(prompt, default)


    def create_profile(self) -> Profile | None:
        """Create and save a profile for the given config.

        Returns:
            A `Profile` obj containing axe config data or `None` if the user
            enters a cancel command.
        """
        # TODO Render text about defaults, axe types, etc
        try:  # Prompt user for Profile config values
            self.print("Enter [red][!!][/] at any time to cancel")  # escape hatch
            profile_name = Prompt.ask("Enter a [green]profile name[/]:",
                                      default="Default")
            assert profile_name != "!!"  # Allows user to cancel at any time

            hostname = Prompt.ask("Enter [green]hostname[/] (Optional):",
                                  default="Unknown")
            assert hostname != "!!"

            frequency = self._validate_int_prompt("Enter [green]frequency:",
                                                  default=575)
            assert frequency

            c_voltage = self._validate_int_prompt("Enter [green]coreVoltage:",
                                                  default=1150)
            assert c_voltage

            fanspeed = self._validate_int_prompt("Enter [green]fanspeed:",
                                                 default=100)
            assert fanspeed

        except AssertionError:
            self.print("[blue]Canceling profile creation... ⏳")
            return

        try: # Return a Profile() and save the config file
            profile = Profile.create_profile(
                {"profile_name": profile_name, "hostname": hostname,
                 "frequency": frequency, "coreVoltage": c_voltage,
                 "fanspeed": fanspeed}
            )
            profile.save_profile(profile_dir=self.profile_dir)
            assert path.exists(f"{self.profile_dir}{profile.name}.json")

            self.print(f"Profile [blue]{profile.name} created! 🍞")
            return profile
        except AssertionError:
            print("Error verifying profile was saved")
        except Exception as e:
            raise e

    def session(self) -> None:
        # Handle user choice
        self.main_menu()
        user_choice = Prompt.ask(
            "Enter an option ([italics]not case sensitive[/]):",
            choices=['L', 'N', 'U', 'R', 'D', 'M', 'Q'],
            default='M',
            case_sensitive=False
        )

        # Run session loop via recursion
        match user_choice.lower():
            case 'l':
                # # TODO separate/check by axe type (single-chip, multi-chip)
                self.print(f"[green][{user_choice}][/] >>> Listing profiles")
                # sleep(0.3)
                self.list_profiles()
                self.session()
            case 'n':
                # TODO new profile (n)
                self.print(f"[green][{user_choice}][/] >>> Creating profile")
                # sleep(0.3)
                # TODO Use the obj? Selection (default)?
                self.create_profile()
                sleep(1.5)
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
