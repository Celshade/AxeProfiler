# Source: ESP-Miner
# https://github.com/bitaxeorg/ESP-Miner/blob/master/main/http_server/openapi.yaml

HTTP = "http://"
API = {
    # NOTE: Valid route, but not yet used by this program
    "scan": {  # scan for available networks (not axes)
        "type": "GET",
        "url": "/api/system/wifi/scan"
    },
    "info": {
        "type": "GET",
        "url": "/api/system/info"
    },
    # NOTE: Valid route, but not yet used by this program
    "asic": {
        "type": "GET",
        "url": "/api/system/asic"
    },
    "statistics": {
        "type": "GET",
        "url": "/api/system/statistics"
    },
    # NOTE: Valid route, but not yet used by this program
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
    # NOTE: Valid route, but not yet used by this program
    "firmware": {  # NOTE: [requestBody] update firmware
        "type": "POST",
        "url": "/api/system/OTA"
    },
    # NOTE: Valid route, but not yet used by this program
    "website": {  # NOTE: [requestBody] update website firmware
        "type": "POST",
        "url": "/api/system/OTAWWW"
    }
}
