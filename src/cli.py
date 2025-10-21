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
        # TODO show existing profiles (e)
        # # TODO select/view profiles
        # # # TODO separate/check by axe type (single-chip, multi-chip)
        # TODO create new profile (n)
        # TODO update profile (u)
        # TODO delete profile (d)
        # TODO run profile (r)
        # # TODO apply to multiple devices?
        # TODO show this menu again (m)
        # TODO quit (q)

        # Handle user choice
        user_choice = Prompt.ask("Select an option (not case sensitive): ",
                                 choices=['E', 'N', 'U', 'D', 'R', 'M', 'Q'],
                                 default='M',
                                 case_sensitive=False)
        print(user_choice)


# NOTE: Testing
if __name__ == "__main__":
    cli = Cli()
    cli.menu()
