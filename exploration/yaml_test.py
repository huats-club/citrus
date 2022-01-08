import os

import yaml

if __name__ == "__main__":

    # Test yaml dumping
    out = {
        "coverage": {
            "workspace": "workspace/01-08-2022_15-48-00",
            "private": "workspace/01-08-2022_15-48-00/cached",
            "heatmaps": {
                "NOKIA-2291": "workspace/01-08-2022_15-48-00/cached/scaled_NOKIA-2291_1.png",
                "SINGTEL-F772": "workspace/01-08-2022_15-48-00/cached/scaled_SINGTEL-F772_2.png",
                "Combined": "workspace/01-08-2022_15-48-00/cached/scaled_Combined_3.png"
            },
            "current_tab": "WIFI",
            "tracked": [
                {
                    "bssid": "08:9b:b9:1c:22:9a",
                    "channel_frequency": "2462",
                    "channel_number": "11",
                    "channel_width": "20",
                    "rssi": "-67",
                    "ssid": "NOKIA-2291"
                },
                {
                    "bssid": "4c:1b:86:6c:f7:72",
                    "channel_frequency": 0,
                    "channel_number": 0,
                    "channel_width": 0,
                    "rssi": -100,
                    "ssid": "SINGTEL-F772"
                }
            ],
            "recorded_points": [
                {
                    "x": 465,
                    "y": 312,
                    "data": [
                        {
                            "ssid": "NOKIA-2291",
                            "rssi": -64
                        },
                        {
                            "ssid": "SINGTEL-F772",
                            "rssi": -100
                        }
                    ]
                },
                {
                    "x": 694,
                    "y": 499,
                    "data": [
                        {
                            "ssid": "NOKIA-2291",
                            "rssi": -68
                        },
                        {
                            "ssid": "SINGTEL-F772",
                            "rssi": -100
                        }
                    ]
                },
                {
                    "x": 667,
                    "y": 251,
                    "data": [
                        {
                            "ssid": "NOKIA-2291",
                            "rssi": -68
                        },
                        {
                            "ssid": "SINGTEL-F772",
                            "rssi": -100
                        }
                    ]
                },
                {
                    "x": 544,
                    "y": 402,
                    "data": [
                        {
                            "ssid": "NOKIA-2291",
                            "rssi": -68
                        },
                        {
                            "ssid": "SINGTEL-F772",
                            "rssi": -100
                        }
                    ]
                },
                {
                    "x": 788,
                    "y": 136,
                    "data": [
                        {
                            "ssid": "NOKIA-2291",
                            "rssi": -67
                        },
                        {
                            "ssid": "SINGTEL-F772",
                            "rssi": -100
                        }
                    ]
                },
                {
                    "x": 255,
                    "y": 196,
                    "data": [
                        {
                            "ssid": "NOKIA-2291",
                            "rssi": -67
                        },
                        {
                            "ssid": "SINGTEL-F772",
                            "rssi": -100
                        }
                    ]
                },
                {
                    "x": 984,
                    "y": 519,
                    "data": [
                        {
                            "ssid": "NOKIA-2291",
                            "rssi": -67
                        },
                        {
                            "ssid": "SINGTEL-F772",
                            "rssi": -100
                        }
                    ]
                }
            ]
        }
    }
    with open(os.getcwd() + "/exploration/yaml_data/write.yaml", "w") as f:
        data = yaml.dump(out, f)

    # Test yaml loading
    with open(os.getcwd() + "/exploration/yaml_data/write.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        print(data)
