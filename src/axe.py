from pprint import pprint

import requests

from api import API


HTTP = "http://"


def request(ip: str, endpoint: str):
    api = API[endpoint]

    if api["type"] == "GET":
        return requests.get(f"{HTTP}{device_ip}{api['url']}")
    elif api["type"] == "POST":
        return requests.post(f"{HTTP}{device_ip}{api['url']}")
    elif api["type"] == "PATCH":
        return requests.patch(f"{HTTP}{device_ip}{api['url']}")
    else:
        raise NotImplementedError("Not yet available")


if __name__ == "__main__":
    device_ip = input("Enter IP: ")
    res = request(device_ip, "info")
    pprint(res.json())
