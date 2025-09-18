from os import rename
from typing import Self
import json


class Profile():
    """A representation of a Profile able to be used by a miner running AxeOS.
    """
    def __init__(
            self,
            name: str,
            frequency: int,
            coreVoltage: int,
            fanspeed: int):
        self._name = name
        self._frequency = frequency
        self._coreVoltage = coreVoltage
        self._fanspeed = fanspeed

    def __repr__(self):
        return ' '.join((
            f"Profile({self._name},",
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
            "name": self._name,
            "frequency": self._frequency,
            "coreVoltage": self._coreVoltage,
            "fanspeed": self._fanspeed
        }

    @classmethod
    def create_profile(cls, config: dict[str, str]) -> Self:
        """Create and return a new instance of `Profile` for the given config.

        The ncecessary class instantiation data (name, frequency, coreVoltage,
        fanspeed) will be validated and taken from the `config` argument -
        additional data may be included in the config, but it will not persist
        in the object being returned.

        Args:
            config: A dict of config data to create the Profile from.
        """
        profile_data = {}

        # Validate each of the necessary Profile params
        if "name" in config and isinstance(config["name"], str):
            profile_data["name"] = config["name"]
        else:
            raise ValueError("Missing or incorrect format for `name`")

        if "frequency" in config and isinstance(config["frequency"], int):
            profile_data["frequency"] = config["frequency"]
        else:
            raise ValueError("Missing or incorrect format for `frequency`")

        if "coreVoltage" in config and isinstance(config["coreVoltage"], int):
            profile_data["coreVoltage"] = config["coreVoltage"]
        else:
            raise ValueError("Missing or incorrect format for `coreVoltage`")

        if "fanspeed" in config and isinstance(config["fanspeed"], int):
            profile_data["fanspeed"] = config["fanspeed"]
        else:
            raise ValueError("Missing or incorrect format for `fanspeed`")

        return cls(
            name=profile_data["name"],
            frequency=profile_data["frequency"],
            coreVoltage=profile_data["coreVoltage"],
            fanspeed=profile_data["fanspeed"]
        )

    def validate_profile(self) -> bool:
        return False  # TODO implement

    def update_profile(
            self,
            name: str = None,
            frequency: int = None,
            coreVoltage: int = None,
            fanspeed: int = None
        ) -> None:
        return NotImplementedError

    def save_profile(self):
        raise NotImplementedError

    def run_profile(self):
        raise NotImplementedError

    def delete_profile(self):
        raise NotImplementedError
