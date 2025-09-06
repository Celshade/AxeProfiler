from pprint import pprint
import json
import os

import requests

from api import HTTP, API

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
    profile_data = {
        key: data[key] for key in data.keys() & (
            "hostname", "frequency", "coreVoltage", "fanspeed"
        )
    }
    print(profile_data)  # TODO comment out
    return profile_data


def ensure_profile_dir() -> None:
    """Check for an existing profiles dir and create one if needed.
    """
    try:
        if not os.path.isdir("./profiles"):
            os.mkdir("./profiles")
            assert os.path.exists("./profiles")
            print("No existing profiles dir found - created profiles dir.")
        else:
            print("Profiles dir already exists 👍🏽")
    except AssertionError:
        print("Failed to confirm or create a profiles dir.")


if __name__ == "__main__":
    device_ip = input("Enter IP: ")
    config = get_current_config(ip=device_ip)
    ensure_profile_dir()
