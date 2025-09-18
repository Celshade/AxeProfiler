from os import rename
import json


class Profile():
    """
    """
    def __init__(self, name: str, frequency: int, coreVoltage: int):
        self._name = name
        self._frequency = frequency
        self._coreVoltage = coreVoltage

    def __repr__(self):
        return f"Profile({self._name}, {self._frequency}, {self._coreVoltage})"

    def __str__(self):
        return json.dumps(self.data, indent=4)

    @property
    def data(self):
        return {
            "name": self._name,
            "frequency": self._frequency,
            "coreVoltage": self._coreVoltage
        }

    def validate_profile(self) -> bool:
        return 

    @data.setter
    def data(self, new_data: dict):
        if "name" in new_data and isinstance(new_data["name"], str):
            self._name == new_data["name"]
            print(f"Upda {self._name}")
        
        if "frequency" in new_data and isinstance(new_data["frequency"], str):
            self._name == new_data["frequency"]
        
        if "coreVoltage" in new_data and isinstance(new_data["coreVoltage"], str):
            self._name == new_data["coreVoltage"]



        if "name" in new_data:
            self._name = new_data["name"]
        else:
            print("no name")
        # self._name = new_data.get("name") or self._name
        # self._frequency = new_data.get("frequency") or self._frequency
        # self._coreVoltage = new_data.get("coreVoltage") or self._coreVoltage

        # if name:
        #     self._data["name"] = name
        # if frequency:
        #     self._data["frequency"] = frequency
        # if coreVoltage:
        #     self._data["coreVoltage"] = coreVoltage


    def update_profile(
            self,
            name: str = None,
            frequency: str = None,
            coreVoltage: str = None
        ) -> None:
        """
        """
        return NotImplementedError

    # def save_profile(self):
    #     try:
    #         assert all(self._data[i] for i in self._data)
    #         with open(f"{self._data['name']}", 'w'):

    #     except AssertionError:
    #         print("No profile name set - cannot save profile.")

    def run_profile(self):
        raise NotImplementedError

    def delete_profile(self):
        raise NotImplementedError