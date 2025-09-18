import json
import os

import requests

from api import HTTP, API
from profiles import Profile

# Response obj from AxeOS API GET /api/system/info
AXE_INFO_OBJ = dict[str, str | int | list[dict[str, str | int]]]


# TODO handle invalid/unknown IP
def request(
        ip: str,
        endpoint: str,
        body: dict | None = None
) -> requests.Response | None:  # TODO update return annotation if using .json()
    """Make and return the proper request for the given IP addr and endpoint.

    Args:
        ip: The IP of the [axe] device.
        endpoint: The desired AxeOS endpoint to hit.
        body: The body data to send with PATCH/POST requests (default=None).

    Returns:
        A `requests.Response` response object else `None`
    """

    try:
        method, url = API[endpoint]["type"], f"{HTTP}{ip}{API[endpoint]['url']}"

        if method == "GET":
            res = requests.get(url)

            if res.status_code == 200:
                return res.json()
            raise ValueError(res.status_code)
        elif method == "POST":
            raise NotImplementedError  # TODO Implement `body`
            # return requests.post(url)
        elif method == "PATCH":
            # return requests.patch(url)
            raise NotImplementedError  # TODO Implement `body`
        else:
            raise ValueError("Not a valid HTTP method for this API.")
    except ValueError as ve:
        print(f"Request error: HTTP {ve} for {method} {url}")
        return None
    except Exception as e:
        print(f"Unknown error: {e} for {method} {url}")
        return None


def get_current_config(ip: str) -> dict[str, str]:
    """
    """
    # Get existing freq/c.volt
    data = request(ip, "info")
    # pprint(data)
    profile_data = {
        key: data[key] for key in data.keys() & (
            "hostname", "frequency", "coreVoltage", "fanspeed"
        )
    }
    profile_data["IP"] = ip

    print(profile_data)  # TODO remove
    return profile_data


def check_for_profiles() -> None:
    """Check for an existing `profiles` dir and create one if needed.
    """
    try:
        if not os.path.isdir("./profiles"):
            os.mkdir("./profiles")
            assert os.path.exists("./profiles")
            print("No profiles dir found - creating local profiles dir at . ✅")
        elif num_profiles := len(os.listdir("./profiles")):
            # TODO enhance verification?
            print(f"{num_profiles} existing profiles found! ✅")
        else:
            print("`Profiles` dir exists, but no profiles found 📂")
    except AssertionError:
        print("Failed to create a `profiles` dir 😢")


def create_profile(
        config: dict[str, str],
        profile_name: str | None = None
    ) -> Profile | None:
    """Create and save a profile for the given config.

    Args:
        config: The config data to save to the profile.
        profile_name(optional): The profile name (default=None).
    Returns:
        A profile object/dict containing axe config data.
    """
    try:
        check_for_profiles()
        profile = Profile.create_profile(
            {
                "profile_name": profile_name or input(
                    "Enter a name for this profile: "
                ),
                **config
            }
        )
        # print(profile, type(profile))  # TODO remove
        # TODO move this into Profile.save_profile()
        with open(f"./profiles/{profile.name}.json", 'w') as f:
            f.write(json.dumps(profile.data, indent=4))

        assert os.path.exists(f"./profiles/{profile.name}.json")  # TODO remove
        print(f"Profile: {profile.name} created! ✅")
        return profile
    except AssertionError:
        print("Error verifying profile was saved")
    except Exception as e:
        raise e


def load_profile(profile_name: str) -> dict[str, str]:
    """Load an existing profile.

    Args:
        profile_name: The name of the profile to load.
    """
    try:
        print("Loading profile... ⏳")
        with open(f"./profiles/{profile_name}.json", 'r') as f:
            profile = json.loads(f.read())  # TODO turn into a Profile() obj?

        return profile
    except FileNotFoundError as fe:
        print(f"Could not find a profile named: {profile_name} ⚠")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    device_ip = "192.168.0.2"  # input("Enter IP: ")  # NOTE testing IP only
    config = get_current_config(ip=device_ip)
    profile = create_profile(config=config)
    print(profile)

    print(end='\n')
    updated_profile = load_profile(profile.name)
    print(updated_profile == profile.data)  # TODO remove

    print()
    print(profile.__repr__())
