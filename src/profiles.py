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

from os import path, rename, remove
from typing import Self
from time import sleep
import json

from api import request


def validate_profile(profile_name: str) -> bool:
    """Return True if the saved profile already exists else False."""
    return path.exists(f"./.profiles/{profile_name}.json")


class Profile():
    """Representation of a device config used by a miner running AxeOS."""
    def __init__(self,
                 profile_name: str, hostname: str,
                 frequency: int, coreVoltage: int, fanspeed: int):
        self._name = profile_name
        self._hostname = hostname
        self._frequency = frequency
        self._coreVoltage = coreVoltage
        self._fanspeed = fanspeed

    def __repr__(self):
        return ' '.join((
            f"Profile({self._name},",
            f"{self._hostname},",
            f"{self._frequency},",
            f"{self._coreVoltage},",
            f"{self._fanspeed})",
        ))

    def __str__(self):
        return json.dumps(self.data, indent=4)

    @property
    def name(self) -> str:
        """Return the profile name."""
        return self._name

    @property
    def hostname(self) -> str:
        """Return the device name."""
        return self._hostname

    @property
    def frequency(self) -> int:
        """Return the profile frequency setting."""
        return self._frequency

    @property
    def coreVoltage(self) -> int:
        """Return the profile core voltage setting."""
        return self._coreVoltage

    @property
    def fanspeed(self) -> int:
        """Return the profile fan speed setting."""
        return self._fanspeed

    @property
    def data(self) -> dict[str, str | int]:
        """Return a dict of profile data (JSON compatible)."""
        return {
            "profile_name": self._name,
            "hostname": self._hostname,
            "frequency": self._frequency,
            "coreVoltage": self._coreVoltage,
            "fanspeed": self._fanspeed
        }

    @classmethod
    def validate_profile_data(
            cls, config: dict[str, str | int]) -> dict[str, str | int]:
        """Validate and return a config dict for creating/updating Profiles.

        Only data used by `Profile` instantiation will be persisted in the
        returned `dict` after type validation. NOTE: This method is only
        intended for use in creating `Profile` objects - see
        `Profile.update_profile()` for updates to existing profiles.

        Args:
            config: A dict of config data to create the Profile from.
        Returns:
            A dict of data validated for use in `Profile` creation.
        """
        profile_data = {}  # container for validated data

        if (config.get("profile_name")
                and isinstance(config["profile_name"], str)):
            profile_data["profile_name"] = config["profile_name"]
        else:
            raise ValueError("Missing or incorrect type for `profile_name`")

        if (config.get("hostname") and isinstance(config["hostname"], str)):
            profile_data["hostname"] = config["hostname"]
        else:
            raise ValueError("Missing or incorrect type for `hostname`")

        if (config.get("frequency") and isinstance(config["frequency"], int)):
            profile_data["frequency"] = config["frequency"]
        else:
            raise ValueError("Missing or incorrect type for `frequency`")

        if (config.get("coreVoltage")
                and isinstance(config["coreVoltage"], int)):
            profile_data["coreVoltage"] = config["coreVoltage"]
        else:
            raise ValueError("Missing or incorrect type for `coreVoltage`")

        if (config.get("fanspeed") and isinstance(config["fanspeed"], int)):
            profile_data["fanspeed"] = config["fanspeed"]
        else:
            raise ValueError("Missing or incorrect type for `fanspeed`")

        return profile_data

    @classmethod
    def create_profile(cls, config: dict[str, str]) -> Self:
        """Create and return a new instance of `Profile` for the given config.

        The ncecessary class instantiation data (name, frequency, coreVoltage,
        fanspeed) will be passed to a validation function prior to object
        instantiation.

        Args:
            config: A dict of config data to create the Profile from.
        Returns:
            Returns a new `Profile`.
        Raises:
            AttributeError: if config data failes validation.
        """
        try:
            return cls(**cls.validate_profile_data(config))
        except Exception:
            raise AttributeError("Profile could not be created 😭")

    def update_profile(self, updates: dict[str, str | int]) -> None:
        """Update the profile config and save the changes.

        Only attrs used by `Profile` will be saved. Unlike
        `cls.validate_profile_data()`, this method supports partial updates
        to existing profiles and does not require every attr to be passed.

        Args:
            updates: A `dict` of config data to update the `Profile` with.
        """
        try:
            og_name = None  # Will retain the original name if name changes
            updated = False  # Flag to trigger saving

            # Reassign profile attrs if any are modified.
            print("Checking for profile updates...⏳")
            if profile_name := updates.get("profile_name"):
                if profile_name != self.name:
                    print("Updating profile name: "
                          + f"{self.name} -> {profile_name}")
                    og_name, self._name = self.name, profile_name
                    updated = True

            if hostname := updates.get("hostname"):
                if hostname != self.hostname:
                    print("Updating device name: "
                          + f"{self.hostname} -> {hostname}")
                    self._hostname = hostname
                    updated = True

            if frequency := updates.get("frequency"):
                if frequency != self.frequency:
                    print("Updated frequency: "
                          + f"{self.frequency} -> {frequency}")
                    self._frequency = frequency
                    updated = True

            if cVoltage := updates.get("coreVoltage"):
                if cVoltage != self.coreVoltage:
                    print("Updating coreVoltage: "
                        + f"{self.coreVoltage} -> {cVoltage}")
                    self._coreVoltage = updates.get("coreVoltage")
                    updated = True

            if fanspeed := updates.get("fanspeed"):
                if fanspeed != self.fanspeed:
                    print(f"Updating frequency: {self.fanspeed} -> {fanspeed}")
                    self._fanspeed = updates.get("fanspeed")
                    updated = True

            if updated:
                print("Saving profile updates...⏳")
                self.save_profile(replace_profile=og_name if og_name else None)
            else:
                print("Nothing to update")
        except Exception as e:
            raise e

    def save_profile(self, profile_dir: str, replace_profile: str | None = None):
        try:
            if replace_profile and validate_profile(replace_profile):
                existing_filename = f"{profile_dir}{replace_profile}.json"
                with open(existing_filename, 'w') as f:
                    f.write(json.dumps(self.data, indent=4))

                # Rename the existing file
                rename(existing_filename, f"{profile_dir}{self.name}.json")
            with open(f"{profile_dir}{self.name}.json", 'w') as f:
                f.write(json.dumps(self.data, indent=4))
        except Exception as e:
            raise e

    def run_profile(self, ip: str, update: bool = False) -> None:
        """Apply profile settings to the device.

        Sends the profile configuration to the device. If `update` is True, the
        frequency, coreVoltage, and fanspeed settings are pushed to the device;
        otherwise, the device is simply restarted.

        Args:
            ip: The IP address of the device to apply the profile to.
            update: If True, update the device configuration (default=False).

        Raises:
            requests.HTTPError: If there is an error in the API requests.
        """
        # TODO check logic around push vs restart (push will also restart)
          # Check when are we not pushing?
        # try:
        if update:
            push_data = {
                    k:self.data[k] for k in self.data
                    if k not in ("profile_name", "hostname")
                }
            # print(push_data)
            res = request(ip=ip, endpoint="system", body=push_data)
            print("System updated ✅")
        else:
            res = request(ip=ip, endpoint="restart")
            print("Device restarted ✅")
        # except Exception as e:
        #     print("Error - could not run profile ⚠")
        #     raise e
