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
from time import sleep
from typing import TypeAlias
from os import system, path, mkdir, listdir

from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.console import Console


CONFIG: TypeAlias = dict[str, str | int]  # config obj format


class Cli(Console):
    def __init__(self) -> None:
        super().__init__()  # Inherit Console() ability to render/color
        self._profile_dir: str | None

        # Check for a profile_dir specified in the config file
        try:
            if path.exists(".config"):
                with open(".config", 'r') as f:
                    config: CONFIG = json.loads(f.read())

                if profile_dir := config.get("profile_dir"):
                    assert profile_dir and isinstance(profile_dir, str)
                    self._profile_dir = profile_dir
                    return
        except AssertionError:
            pass

        # TODO implement/fix
        # Check for or create local profile dir
        msg = "[purple]Invalid profile directory found in [blue].config"
        # Check for local profile dir (create if none)
        if not self._profile_dir and path.isdir(self.profile_dir):
            self.print("[green]No profiles found "
                        + "[green]creating local profiles directory at .")
            mkdir(".profiles/")
            assert path.exists(".profiles/")




    @property
    def profile_dir(self) -> str:
        return self._profile_dir

    @property
    def num_profiles(self) -> int | None:
        try:

            return len(listdir(self.profile_dir))
        except AssertionError:
            print("Failed to find or create a `profiles` dir 😢")

    def show_notice(self) -> None:
        try:
            system("clear")  # NOTE @Linux; handle MAC/Windows

            # raise FileNotFoundError  # TESTING
            assert path.exists(".notice")
            with open(".notice", 'r') as f:
                notice = f.read()

            self.print(Panel(notice, title="[bold bright_cyan]Copyright Notice",
                            width=80))
            sleep(4.2)  # Let the user at least skim over the notice
        except FileNotFoundError:
            msg = ''.join(("Could not render the [red]copyright[/] notice.\n",
                            "Please see line 4 of any source file or ",
                            "[red]COPYING[/] for more details."))
            self.print(Panel(msg, title="[bold bright_cyan]Copyright Notice",
                            width=80))
            sleep(4.2)  # Let the user at least skim over the notice

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
