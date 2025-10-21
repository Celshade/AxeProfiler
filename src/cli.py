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


class Cli():
    # def __init__(self):
    #     return self

    def menu(self):
        # TODO show copyright notice on menu start
        # Handle user choice
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
                print(">>>Menu")
            case 'q':
                # TODO quit (q)
                print(">>>Session Terminated")


# NOTE: Testing
if __name__ == "__main__":
    cli = Cli()
    cli.menu()
