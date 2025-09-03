
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
