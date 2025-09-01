from pprint import pprint

import requests


HTTP = "http://"
API = {
    "scan": {  # scan for axes on network
        "type": "GET",
        "url": "/api/system/wifi/scan"
    },
    "info": {
        "type": "GET",
        "url": "/api/system/info"
    },
    "asic": {
        "type": "GET",
        "url": "/api/system/asic"
    },
    "statistics": {
        "type": "GET",
        "url": "/api/system/statistics"
    },
    "dashboard": {
        "type": "GET",
        "url": "/api/system/statistics/dashboard"
    },
    "restart": {
        "type": "POST",
        "url": "/api/system/restart"
    },
    "system": {  # NOTE: requestBody change system settings
        "type": "PATCH",
        "url": "/api/system"
    },
    "firmware": {  # NOTE: [requestBody] update firmware
        "type": "POST",
        "url": "/api/system/OTA"
    },
    "website": {  # NOTE: [requestBody] update website firmware
        "type": "POST",
        "url": "/api/system/OTAWWW"
    }

}


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
