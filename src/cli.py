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

from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
from rich.console import Console


class Cli(Console):
    def __init__(self):
        super().__init__()  # Inherit console ability to print/etc objects

    def show_notice(self) -> None:
        # TODO show copyright once on init
        raise NotImplementedError

    def _create_menu(self) -> None:
        menu = Table(title="[green]Enter one of the following options",
                     width=80)

        menu.add_column("Option", width=0)
        menu.add_column("Description", width=6)

        menu.add_row("[green]L", "List all of the available Profiles")
        menu.add_row("[green]N", "Create a new Profile")
        menu.add_row("[green]U", "Update an existing Profile")
        menu.add_row("[green]R", "Run an existing Profile")
        menu.add_row("[green]D", "Delete an existing Profile")
        menu.add_row("[green]M[white] (default)", "Show this menu again")
        menu.add_row("[red]Q", "Exit the program")
        return menu

    def main_menu(self) -> None:
        menu = self._create_menu()
        rprint(Panel(menu, title="[cyan]Main Menu", width=80))


    def main(self):
        # Handle user choice
        self.main_menu()
        user_choice = Prompt.ask("Select an option (not case sensitive): ",
                                 choices=['L', 'N', 'U', 'R', 'D', 'M', 'Q'],
                                 default='M',
                                 case_sensitive=False)
        print(user_choice)
        match user_choice.lower():
            case 'l':
                # TODO List existing profiles (L)
                # # TODO separate/check by axe type (single-chip, multi-chip)
                print(">>>Listing profiles")
            case 'n':
                # TODO new profile (n)
                print(">>>Creating new profile")
            case 'u':
                # TODO update profile (u)
                print(">>>Updating profile")
            case 'r':
                # TODO run profile (r)
                # # NOTE apply to multiple devices?
                print(">>>Running profile")
            case 'd':
                # TODO delete profile (d)
                print(">>>Deleting profile")
            case 'm':
                # TODO show this menu again (m)
                self.main_menu()
            case 'q':
                # TODO quit (q)
                print(">>>Session Terminated")



# NOTE: Testing
if __name__ == "__main__":
    cli = Cli()
    cli.main()
