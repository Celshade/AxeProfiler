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

import unittest
from unittest.mock import patch
from io import StringIO
from src.cli import Cli


class TestCli(unittest.TestCase):
    def setUp(self):
        self.cli = Cli()

    def test_show_notice(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cli.show_notice()
            output = fake_out.getvalue()
            self.assertIn("copyright notice line 1", output)
            self.assertIn("Line 2", output)

    def test_create_menu_structure(self):
        menu = self.cli._create_menu()
        self.assertEqual(menu.title,
                         "[green]Enter one of the following options")
        self.assertEqual(menu.width, 76)
        self.assertEqual(len(menu.columns), 2)  # Option and Description columns
        self.assertEqual(len(menu.rows), 7)  # L,N,U,R,D,M,Q options

    def test_main_menu_clears_screen(self):
        with patch('os.system') as mock_system:
            self.cli.main_menu()
            mock_system.assert_called_once_with('clear')

    @patch('rich.prompt.Prompt.ask')
    def test_session_list_profiles(self, mock_ask):
        mock_ask.side_effect = ['L', 'Q']  # List then Quit
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cli.session()
            output = fake_out.getvalue()
            self.assertIn("Listing profiles", output)
            self.assertIn("Session Terminated", output)

    @patch('rich.prompt.Prompt.ask')
    def test_session_new_profile(self, mock_ask):
        mock_ask.side_effect = ['N', 'Q']
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cli.session()
            output = fake_out.getvalue()
            self.assertIn("Creating profile", output)

    @patch('rich.prompt.Prompt.ask')
    def test_session_update_profile(self, mock_ask):
        mock_ask.side_effect = ['U', 'Q']
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cli.session()
            output = fake_out.getvalue()
            self.assertIn("Updating profile", output)

    @patch('rich.prompt.Prompt.ask')
    def test_session_run_profile(self, mock_ask):
        mock_ask.side_effect = ['R', 'Q']
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cli.session()
            output = fake_out.getvalue()
            self.assertIn("Running profile", output)

    @patch('rich.prompt.Prompt.ask')
    def test_session_delete_profile(self, mock_ask):
        mock_ask.side_effect = ['D', 'Q']
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cli.session()
            output = fake_out.getvalue()
            self.assertIn("Deleting profile", output)

    @patch('rich.prompt.Prompt.ask')
    def test_session_show_menu(self, mock_ask):
        mock_ask.side_effect = ['M', 'Q']
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cli.session()
            output = fake_out.getvalue()
            self.assertIn("Returning to menu", output)

    @patch('rich.prompt.Prompt.ask')
    def test_session_quit(self, mock_ask):
        mock_ask.side_effect = ['Q']
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cli.session()
            output = fake_out.getvalue()
            self.assertIn("Session Terminated", output)

    @patch('rich.prompt.Prompt.ask')
    def test_session_case_insensitive(self, mock_ask):
        mock_ask.side_effect = ['q']  # lowercase should work
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cli.session()
            output = fake_out.getvalue()
            self.assertIn("Session Terminated", output)

    @patch('rich.prompt.Prompt.ask')
    def test_session_default_option(self, mock_ask):
        mock_ask.side_effect = ['', 'Q']  # Empty input should default to 'M'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cli.session()
            output = fake_out.getvalue()
            self.assertIn("Returning to menu", output)


if __name__ == '__main__':
    unittest.main()
