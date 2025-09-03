from pprint import pprint
# import json

import requests

from api import HTTP, API


def request(ip: str, endpoint: str) -> requests.Response | None:
    """Make and return the proper request for the given IP addr and endpoint.

    Args:
        ip: The IP of the [axe] device.
        endpoint: The desired AxeOS endpoint to hit.

    Returns:
        A `requests.Response` response object else `None`
    """

    try:
        method, url = API[endpoint]["type"], f"{HTTP}{ip}{API[endpoint]['url']}"

        if method == "GET":
            return requests.get(url)
        elif method == "POST":
            body = {}  # TODO Implement
            return requests.post(url)
        elif method == "PATCH":
            body = {}  # TODO Implement
            return requests.patch(url)
        else:
            raise ValueError("Not a valid HTTP method for this API.")
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    device_ip = input("Enter IP: ")
    res = request(device_ip, "info")
    pprint(res.json())
