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

from os import system
from time import sleep

from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.console import Console


class Cli(Console):
    def __init__(self):
        super().__init__()  # Inherit console ability to print/etc objects

    def show_notice(self) -> None:
        # TODO show copyright once on init
        with open(".notice", 'r') as f:
            notice = f.read()
        self.print(Panel(notice, title="[bold bright_cyan]Copyright Notice",
                         width=80))
        sleep(4.2)


    def _create_menu(self) -> None:
        menu = Table(title="[green]Enter one of the following options",
                     width=76)

        menu.add_column("Option")
        menu.add_column("Description")

        menu.add_row("[bold green]L", "List all of the available Profiles")
        menu.add_row("[bold green]N", "Create a new Profile")
        menu.add_row("[bold green]U", "Update an existing Profile")
        menu.add_row("[bold green]R", "Run an existing Profile")
        menu.add_row("[bold green]D", "Delete an existing Profile")
        menu.add_row(
            "[bold bright_cyan]M[white] (default)", "Show this menu again")
        menu.add_row("[bold red]Q", "Quit the program")
        return menu

    def main_menu(self) -> None:
        system("clear")  # NOTE @Linux; handle MAC/Windows
        menu = self._create_menu()
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
