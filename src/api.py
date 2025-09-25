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
# ---
# The full API spec can be found at:
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
